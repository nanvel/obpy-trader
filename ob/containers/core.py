import time

from dependency_injector import containers, providers

from ob.exchanges.binance import (
    BinanceExchange,
    BinanceStream,
    OrderBookFactory,
    OrderBookUpdatesFactory,
    SymbolFactory,
    TradeFactory,
)
from ob.storage.backends import FsWriter
from ob.storage.factories.file_name import FileNameFactory


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    symbol_factory = providers.Singleton(SymbolFactory)
    order_book_factory = providers.Singleton(OrderBookFactory)
    order_book_updates_factory = providers.Singleton(OrderBookUpdatesFactory)
    trade_factory = providers.Singleton(TradeFactory)
    file_name_factory = providers.Singleton(
        FileNameFactory, prefix=config.storage.prefix, extension=".obpy"
    )

    binance_stream = providers.Factory(
        BinanceStream, url="wss://stream.binance.com:9443/stream"
    )

    binance_exchange = providers.Factory(
        BinanceExchange,
        base_url="https://api.binance.com",
        symbol_factory=symbol_factory,
        order_book_factory=order_book_factory,
        order_book_updates_factory=order_book_updates_factory,
        trade_factory=trade_factory,
        stream=binance_stream,
    )

    fs_writer = providers.Resource(
        FsWriter.init,
        root_path=config.storage.fs_root,
        file_name_factory=file_name_factory,
        ts=int(time.time()),
    )
