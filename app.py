import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.devices.handlers.api import stats
from apps.users.handlers.api import auth
from zmey_gorynych import db


# https://github.com/pyca/bcrypt/issues/684
logging.getLogger('passlib').setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    yield
    await db.shutdown()


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(stats.router)
    app.include_router(auth.api_router)
    return app


if __name__ == '__main__':
    import uvicorn
    app = create_app()
    uvicorn.run(app, host='127.0.0.1', port=8080)
