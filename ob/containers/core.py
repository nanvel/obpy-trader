import time

from dependency_injector import containers, providers

from ob.exchanges.binance import BinanceExchange
from ob.storage.backends import FsReader, FsWriter
from ob.storage.factories.file_name import FileNameFactory

from .binance import BinanceContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    file_name_factory = providers.Singleton(
        FileNameFactory, prefix=config.storage.prefix, extension=".obpy"
    )

    fs_writer = providers.Resource(
        FsWriter.init,
        root_path=config.storage.fs_root,
        file_name_factory=file_name_factory,
        ts=int(time.time()),
    )

    fs_reader = providers.Resource(FsReader.init)

    binance_exchange = providers.Factory(
        BinanceExchange,
        base_url="https://api.binance.com",
        symbol_factory=BinanceContainer.symbol_factory,
        order_book_factory=BinanceContainer.order_book_factory,
        order_book_updates_factory=BinanceContainer.order_book_updates_factory,
        trade_factory=BinanceContainer.trade_factory,
        stream=BinanceContainer.binance_stream,
    )
