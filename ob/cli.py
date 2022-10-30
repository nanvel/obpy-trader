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

    exchange = getattr(container, f"{exchange}_exchange")()

    use_case = WriteObpy(
        build_file_path=container.build_fs_file_path(),
        exchange=exchange,
        symbol_slug=symbol,
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
