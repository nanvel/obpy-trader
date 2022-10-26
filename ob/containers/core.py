from dependency_injector import containers, providers

from ob.exchanges.binance import BinanceExchange, SymbolFactory
from ob.exchanges.service import ExchangesService
from ob.resources.http_client import init_http_client
from ob.storage.backends import FsWriter


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    symbol_factory = providers.Singleton(SymbolFactory)

    http_client = providers.Resource(init_http_client)

    binance_exchange = providers.Factory(
        BinanceExchange,
        base_url="https://api.binance.com",
        symbol_factory=symbol_factory,
        http_client=http_client,
    )

    exchanges_service = providers.Factory(
        ExchangesService, exchanges=providers.List(symbol_factory)
    )

    fs_writer = providers.Resource(
        FsWriter.init,
        path=
    )
