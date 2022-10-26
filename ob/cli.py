import asyncio

import typer

from ob.containers.core import Container
from ob.settings import Settings


app = typer.Typer()


@app.callback()
def callback():
    """Order Book Trading Framework."""


async def _write_obpy():
    container = Container()

    container.config.from_pydantic(Settings())

    writer = getattr(container, "fs_writer")
    await writer.init()

    writer = await writer()

    try:
        await writer.write(lines=["1", "2"])
    finally:
        await container.shutdown_resources()


@app.command()
def write_obpy():
    asyncio.run(_write_obpy())
