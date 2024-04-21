from fastapi import FastAPI

from apps.devices.handlers.api.stats import router


def create_app():
    app = FastAPI()
    app.include_router(router)
    app.state
    return app


if __name__ == '__main__':
    import uvicorn
    app = create_app()
    uvicorn.run(app, host='127.0.0.1', port=8080)
