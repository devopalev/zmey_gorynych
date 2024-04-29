import asyncio
import glob
import os
import random

from asyncio import AbstractEventLoop, DefaultEventLoopPolicy
from collections.abc import Generator, AsyncGenerator
from contextlib import asynccontextmanager, AbstractAsyncContextManager
from dataclasses import dataclass
from unittest.mock import AsyncMock

import asyncpg
import httpx as httpx
import pytest
import yoyo

from asyncpg import Connection
from asyncpg.transaction import Transaction
from fastapi import FastAPI
from httpx import ASGITransport
from pytest_mock import MockFixture

from pytest_postgresql import factories as postgresql_factories
from pytest_postgresql.executor import PostgreSQLExecutor
from pytest_postgresql.janitor import DatabaseJanitor


postgresql_proc = postgresql_factories.postgresql_proc(
    host='localhost',
    port=random.randint(61000, 65000),
    user='postgres',
)


class EventLoopPolicy(DefaultEventLoopPolicy):
    def __init__(self, event_loop: AbstractEventLoop):
        self.event_loop_for_test = event_loop
        super(EventLoopPolicy, self).__init__()

    def new_event_loop(self) -> AbstractEventLoop:
        return self.event_loop_for_test


loop = asyncio.get_event_loop_policy().new_event_loop()
asyncio.set_event_loop_policy(EventLoopPolicy(loop))


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop_ = asyncio.get_event_loop_policy().new_event_loop()
    yield loop_
    loop_.close()


@pytest.fixture(scope='session')
async def db_conn(
    event_loop: AbstractEventLoop,
    postgresql_proc: PostgreSQLExecutor,
) -> AsyncGenerator[Connection, None]:
    import settings

    db_host = postgresql_proc.host
    db_port = postgresql_proc.port
    db_user = postgresql_proc.user
    db_name = 'testdb'

    db_dsn = f'postgresql://{db_user}@{db_host}:{db_port}/{db_name}'

    # Mock
    settings.DB_DSN = db_dsn

    janitor = DatabaseJanitor(
        user=db_user,
        host=db_host,
        port=str(db_port),
        dbname=db_name,
        version=postgresql_proc.version,
    )
    janitor.init()

    backend = yoyo.get_backend(db_dsn)
    backend.apply_migrations(backend.to_apply(yoyo.read_migrations(os.path.abspath(settings.MIGRATIONS_PATH))))

    conn = await asyncpg.connect(db_dsn)
    yield conn
    await conn.close()

    janitor.drop()


@dataclass
class PoolFake:
    db_conn: Connection

    def acquire(self) -> AbstractAsyncContextManager[Connection]:
        async def get_conn() -> AsyncGenerator[Connection, None]:
            yield self.db_conn

        return asynccontextmanager(get_conn)()


@pytest.fixture()
async def test_db(
    db_conn: Connection,
    mocker: MockFixture,
    event_loop: AbstractEventLoop,
) -> AsyncGenerator[Connection, None]:
    from backend.core import db

    mocker.patch.object(db, 'shutdown_pool', AsyncMock())
    mocker.patch.object(db, 'init_pool', AsyncMock())
    mocker.patch.object(db, 'pool', PoolFake(db_conn))

    tr: Transaction = db_conn.transaction()

    await tr.start()
    yield db_conn
    await tr.rollback()


@pytest.fixture()
async def app(event_loop: AbstractEventLoop, test_db: Connection) -> FastAPI:
    from backend.core.server import create_app

    app = create_app()
    return app


@pytest.fixture()
async def test_client_user(app: FastAPI, event_loop: AbstractEventLoop, base_test_data: None) -> httpx.AsyncClient:
    from backend.apps.users.secure import TokenJWTFactory

    token = TokenJWTFactory(sub='test_user').create_token()

    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://localhost',
        headers={'Authorization': f'{token.type_token} {token.access_token}'},
    ) as client:
        yield client


def db_make_fixture(path: str, recursive: bool = False):  # type: ignore[no-untyped-def]
    @pytest.fixture()
    async def db_fixture(test_db: Connection) -> None:
        files = glob.glob(os.path.abspath(f'tests/{path.lstrip("/")}'), recursive=recursive)
        for file in files:
            with open(file, 'r') as sql:
                await test_db.execute(sql.read())

    return db_fixture


base_test_data = db_make_fixture('/data/base_test_data.sql')
