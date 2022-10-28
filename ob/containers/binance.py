from dependency_injector import containers, providers

from ob.exchanges.binance import (
    BinanceStream,
    OrderBookFactory,
    OrderBookUpdatesFactory,
    SymbolFactory,
    TradeFactory,
)


class BinanceContainer(containers.DeclarativeContainer):
    symbol_factory = providers.Singleton(SymbolFactory)
    order_book_factory = providers.Singleton(OrderBookFactory)
    order_book_updates_factory = providers.Singleton(OrderBookUpdatesFactory)
    trade_factory = providers.Singleton(TradeFactory)

    binance_stream = providers.Factory(
        BinanceStream, url="wss://stream.binance.com:9443/stream"
    )
