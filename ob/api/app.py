from fastapi import FastAPI

from ob.containers.api import ApiContainer
from .routers import cloud, root


def create_app(container: ApiContainer):
    app = FastAPI(title="obpy")
    app.container = container

    app.include_router(cloud.router)
    app.include_router(root.router)

    @app.on_event("startup")
    async def startup_event():
        await container.core.ddb_client.init()

    @app.on_event("shutdown")
    async def shutdown_event():
        await container.shutdown_resources()

    return app
