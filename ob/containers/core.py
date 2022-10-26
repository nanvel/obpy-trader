import time

from dependency_injector import containers, providers

from ob.exchanges.binance import BinanceExchange, SymbolFactory
from ob.resources.http_client import init_http_client
from ob.storage.backends import FsWriter
from ob.storage.factories.file_name import FileNameFactory


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    symbol_factory = providers.Singleton(SymbolFactory)
    file_name_factory = providers.Singleton(
        FileNameFactory, prefix=config.storage.prefix, extension=".obpy"
    )

    http_client = providers.Resource(init_http_client)

    binance_exchange = providers.Factory(
        BinanceExchange,
        base_url="https://api.binance.com",
        symbol_factory=symbol_factory,
        http_client=http_client,
    )

    fs_writer = providers.Resource(
        FsWriter.init,
        root_path=config.storage.fs_root,
        file_name_factory=file_name_factory,
        ts=int(time.time()),
    )
