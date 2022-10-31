import asyncio
import concurrent.futures

import typer

from ob.containers.core import Container
from ob.exchanges.models import ExchangeName
from ob.settings import Settings
from ob.use_cases.write_obpy import WriteObpy


app = typer.Typer()

container = Container()
container.config.from_pydantic(Settings())


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


async def _write_obpy(exchange, symbol_slug):
    exchange = getattr(container, f"{exchange}_exchange")()

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
    asyncio.run(_write_obpy(exchange=exchange, symbol_slug=symbol))


async def _upload_obpy():
    from ob.storage.repositories.fs import FsRepository

    repo = FsRepository(fs_root=container.config.storage.fs_root(), extension=".obpy")
    for file_path in repo.list():
        repo.remove(file_path)


@app.command()
def upload_obpy():
    asyncio.run(_upload_obpy())
