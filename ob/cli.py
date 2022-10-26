import asyncio

import typer

from ob.containers.core import Container
from ob.exchanges.models import ExchangeName
from ob.settings import Settings
from ob.storage.models import StorageName


app = typer.Typer()


@app.callback()
def callback():
    """Order Book Trading Framework."""


async def _write_obpy(exchange, symbol, storage):
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
def write_obpy(
    symbol: str,
    exchange: ExchangeName,
    storage: StorageName = StorageName.FS,
):
    asyncio.run(_write_obpy(exchange=exchange, symbol=symbol, storage=storage))
