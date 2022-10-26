import asyncio

import typer

from ob.containers.core import Container
from ob.exchanges.models import ExchangeName
from ob.settings import Settings
from ob.storage.models import StorageName
from ob.use_cases.write_obpy import WriteObpy


app = typer.Typer()


@app.callback()
def callback():
    """Order Book Trading Framework."""


async def _write_obpy(exchange, symbol, storage):
    container = Container()
    container.config.from_pydantic(Settings())

    exchange = getattr(container, f'{exchange}_exchange')

    writer = getattr(container, f"{storage}_writer")
    await writer.init()

    use_case = WriteObpy(
        writer=await writer(),
        exchange=await exchange(),
        symbol_slug=symbol
    )

    try:
        await use_case.call()
    finally:
        await container.shutdown_resources()


@app.command()
def write_obpy(
    symbol: str = typer.Option(None),
    exchange: ExchangeName = typer.Option(None),
    storage: StorageName = StorageName.FS,
):
    asyncio.run(_write_obpy(exchange=exchange, symbol=symbol, storage=storage))
