import aiohttp
from asyncio import Task, Queue
from urllib.parse import urljoin, urlencode

from ob.models import Symbol

from ..base import BaseExchange
from ..models import ExchangeName
from .factories import SymbolFactory, OrderBookFactory


class BinanceExchange(BaseExchange):
    slug = ExchangeName.BINANCE

    def __init__(
        self,
        symbol_factory: SymbolFactory,
        order_book_factory: OrderBookFactory,
        base_url: str,
    ):
        self.symbol_factory = symbol_factory
        self.order_book_factory = order_book_factory
        self.base_url = base_url

    async def pull_symbol(self, symbol_slug) -> Symbol:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                urljoin(
                    self.base_url,
                    f"/api/v3/exchangeInfo?" + urlencode({"symbol": symbol_slug}),
                )
            ) as response:
                exchange_info = await response.json()

        return self.symbol_factory.from_exchange_info(exchange_info, symbol=symbol_slug)

    async def _pull_order_book(self, symbol: Symbol):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                urljoin(
                    self.base_url,
                    f"/api/v3/depth?"
                    + urlencode({"symbol": symbol.slug, "limit": 5000}),
                )
            ) as response:
                depth = await response.json()

        return self.order_book_factory.from_depth(depth, symbol=symbol)

    async def init_listener(self, symbol: Symbol, queue: Queue) -> Task:
        pass
