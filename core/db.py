import asyncpg
from asyncpg import Pool
from yoyo import get_backend, read_migrations

import settings

pool: Pool | None = None


async def init_pool() -> None:
    global pool
    pool = await asyncpg.pool.create_pool(
        dsn=settings.DB_DSN, min_size=settings.DB_POOL_MIN_SIZE, max_size=settings.DB_POOL_MAX_SIZE
    )


async def shutdown_pool() -> None:
    if pool:
        await pool.close()


async def get_connection() -> asyncpg.Connection:
    if pool:
        async with pool.acquire() as con:
            yield con
    else:
        raise ValueError('pool is not initialized')


def apply_migrations() -> None:
    backend = get_backend(settings.DB_DSN)
    migrations = read_migrations(settings.MIGRATIONS_PATH)

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
