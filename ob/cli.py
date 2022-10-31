import asyncio
import time

import typer

from ob.containers.core import Container
from ob.exchanges.models import ExchangeName
from ob.settings import Settings
from ob.use_cases.write_obpy import WriteObpy


app = typer.Typer()


@app.callback()
def callback():
    """Order Book Trading Framework."""


async def _write_obpy(exchange, symbol_slug):
    container = Container()
    container.config.from_pydantic(Settings())

    exchange = getattr(container, f"{exchange}_exchange")()

    symbol = await exchange.pull_symbol(symbol_slug=symbol_slug)

    write_obpy_uc = WriteObpy(
        obpy_file_factory=container.obpy_file_factory(),
        exchange=exchange,
        symbol=symbol,
    )

    # cloud_repo = await container.cloud_repo()
    # fs_repo = container.fs_repo()
    #
    obpy_file = await write_obpy_uc.call()

    #
    # s3_file_path = container.build_s3_file_path().call(
    #     exchange_slug=exchange.slug,
    #     symbol=symbol,
    #     ts_start=ts_start,
    #     ts_stop=ts_stop,
    # )

    # await cloud_repo.upload(source_path=fs_file_path, target_path=s3_file_path)
    # fs_repo.remove(fs_file_path)
    await container.shutdown_resources()


@app.command()
def write_obpy(
    symbol: str = typer.Option(None), exchange: ExchangeName = typer.Option(None)
):
    asyncio.run(_write_obpy(exchange=exchange, symbol_slug=symbol))


async def _upload_obpy():
    from ob.storage.repositories.fs import FsRepository

    container = Container()
    container.config.from_pydantic(Settings())

    repo = FsRepository(fs_root=container.config.storage.fs_root(), extension=".obpy")
    for file_path in repo.list():
        repo.remove(file_path)


@app.command()
def upload_obpy():
    asyncio.run(_upload_obpy())
