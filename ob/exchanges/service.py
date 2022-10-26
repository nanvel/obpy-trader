import asyncio
from typing import List

from ob.models import ObpyCode

from .base import BaseExchange


class ExchangesService:
    """Yield order book and trades data for specific exchange and symbol."""

    def __init__(self, exchanges: List[BaseExchange]):
        self._exchanges = {i.slug: i for i in exchanges}

    async def run(self, exchange_slug: str, symbol_slug: str, queue: asyncio.Queue):
        exchange = self._exchanges[exchange_slug]
        symbol = await exchange.pull_symbol(symbol_slug=symbol_slug)

        await queue.put(exchange)
        await queue.put(symbol)

        # listener_queue = await exchange.init_listener(symbol=symbol)
        #
        # while True:
        #     message = await listener_queue.get()
        #     if message == ObpyCode.QUIT:
        #         break
        #     await queue.put(message)
        #     assert queue.qsize() < 200
