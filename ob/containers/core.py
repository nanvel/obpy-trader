import time

from dependency_injector import containers, providers

from ob.exchanges.binance import BinanceExchange, SymbolFactory, OrderBookFactory
from ob.storage.backends import FsWriter
from ob.storage.factories.file_name import FileNameFactory


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    symbol_factory = providers.Singleton(SymbolFactory)
    order_book_factory = providers.Singleton(OrderBookFactory)
    file_name_factory = providers.Singleton(
        FileNameFactory, prefix=config.storage.prefix, extension=".obpy"
    )

    binance_exchange = providers.Factory(
        BinanceExchange,
        base_url="https://api.binance.com",
        symbol_factory=symbol_factory,
        order_book_factory=order_book_factory,
    )

    fs_writer = providers.Resource(
        FsWriter.init,
        root_path=config.storage.fs_root,
        file_name_factory=file_name_factory,
        ts=int(time.time()),
    )
