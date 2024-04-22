import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from apps import devices
from apps import users
from core import db

# https://github.com/pyca/bcrypt/issues/684
logging.getLogger('passlib').setLevel(logging.ERROR)


def setup_routes(app: FastAPI) -> None:
    routers = (*devices.routers, *users.routers)

    for r in routers:
        app.include_router(r)

    app.get('/ping')(lambda: JSONResponse({'Success': True}))


@asynccontextmanager
async def lifespan(*args):
    db.apply_migrations()
    await db.init_pool()

    yield

    await db.shutdown_pool()


def create_app():
    app = FastAPI(lifespan=lifespan)
    setup_routes(app)
    return app
