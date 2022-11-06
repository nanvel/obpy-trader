import asyncio
import concurrent.futures

import typer
import uvicorn

from ob.containers.core import Container
from ob.exchanges.models import ExchangeName
from ob.use_cases.write_obpy import WriteObpy


app = typer.Typer()

container = Container()


@app.callback()
def callback():
    """Order Book Trading Framework."""


async def _upload(fs_path, remove_file):
    upload_obpy_file = await container.upload_obpy_file()
    try:
        await upload_obpy_file.call(fs_path=fs_path, remove_file=remove_file)
    finally:
        await container.shutdown_resources()


def upload(fs_path, remove_file=False):
    asyncio.run(_upload(fs_path=fs_path, remove_file=remove_file))


async def _write_obpy(exchange_slug, symbol_slug):
    exchange = getattr(container, exchange_slug).exchange

    symbol = await exchange.pull_symbol(symbol_slug=symbol_slug)

    obpy_file = container.obpy_file_factory().from_symbol(
        exchange_slug=exchange.slug, symbol_slug=symbol.slug
    )

    write_obpy_uc = WriteObpy(
        obpy_file=obpy_file,
        exchange=exchange,
        symbol=symbol,
    )

    try:
        await write_obpy_uc.call()
    finally:
        obpy_file.finalize()

        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as pool:
            await asyncio.get_event_loop().run_in_executor(
                pool, upload, obpy_file.fs_path
            )

        await container.shutdown_resources()


@app.command()
def write_obpy(
    symbol: str = typer.Option(None), exchange: ExchangeName = typer.Option(None)
):
    asyncio.run(_write_obpy(exchange_slug=exchange, symbol_slug=symbol))


@app.command()
def dev_server():
    uvicorn.run(app="ob.server:app", host="0.0.0.0", port=8000, reload=True)


async def _exec_obpy():
    repo = await container.cloud_repo()

    await repo.list(exchange="binance", symbol="BTCUSDT")


@app.command()
def exec_obpy():
    asyncio.run(_exec_obpy())
