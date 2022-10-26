import asyncio

import typer

from ob.containers.core import Container
from ob.settings import Settings
from ob.use_cases.writer_obpy import WriteObpy


app = typer.Typer()


@app.callback()
def callback():
    """Order Book Trading Framework."""


async def _write_obpy():
    container = Container()

    container.config.from_pydantic(Settings())

    try:
        pass
    finally:
        await container.shutdown_resources()

    # await WriteObpy(exchange=).call()


@app.command()
def write_obpy():
    asyncio.run(_write_obpy())
