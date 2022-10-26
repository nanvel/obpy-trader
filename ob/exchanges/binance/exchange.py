import aiohttp
from asyncio import Queue
from urllib.parse import urljoin

from ob.models import Symbol

from ..base import BaseExchange
from .factories import SymbolFactory


class BinanceExchange(BaseExchange):
    slug = "binance"

    # 'https://api.binance.com'
    def __init__(self, symbol_factory: SymbolFactory, base_url: str):
        self.symbol_factory = symbol_factory
        self.base_url = base_url

    async def pull_symbol(self, symbol_slug) -> Symbol:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                urljoin(self.base_url, f"/api/v3/exchangeInfo?symbol={symbol_slug}")
            ) as response:
                exchange_info = await response.json()

        return self.symbol_factory.from_exchange_info(exchange_info, symbol=symbol_slug)

    async def init_listener(self, symbol: Symbol) -> Queue:
        yield "Q"
