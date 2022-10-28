import asyncio

import aiohttp
from asyncio import Queue
from urllib.parse import urlencode, urljoin

from ob.models import Symbol, Trade, OrderBook, OrderBookUpdates

from ..base import BaseExchange
from ..models import ExchangeName
from .factories import (
    OrderBookFactory,
    OrderBookUpdatesFactory,
    SymbolFactory,
    TradeFactory,
)
from .stream import BinanceStream


class BinanceExchange(BaseExchange):
    slug = ExchangeName.BINANCE

    def __init__(
        self,
        symbol_factory: SymbolFactory,
        order_book_factory: OrderBookFactory,
        order_book_updates_factory: OrderBookUpdatesFactory,
        trade_factory: TradeFactory,
        base_url: str,
        stream: BinanceStream,
    ):
        self.symbol_factory = symbol_factory
        self.order_book_factory = order_book_factory
        self.order_book_updates_factory = order_book_updates_factory
        self.trade_factory = trade_factory
        self.base_url = base_url
        self.stream = stream

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

    async def _pull_order_book(self, symbol: Symbol) -> OrderBook:
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

    async def _stream_listener(self, symbol: Symbol, queue: Queue):
        async for row in self.stream.listen(
            subscriptions=[
                f"{symbol.slug.lower()}@depth@100ms",
                f"{symbol.slug.lower()}@aggTrade",
            ]
        ):
            data = row.get("data")
            if not data:
                continue

            if data["e"] == "aggTrade":
                await queue.put(self.trade_factory.from_agg_trade(row))
            elif data["e"] == "depthUpdate":
                await queue.put(self.order_book_updates_factory.from_depth_update(row))

    async def listen(self, symbol: Symbol, queue: Queue):
        updates_queue = Queue()

        asyncio.ensure_future(self._stream_listener(symbol=symbol, queue=updates_queue))
        await asyncio.sleep(0)
        order_book = await self._pull_order_book(symbol=symbol)

        await queue.put(order_book)

        while True:
            update = await updates_queue.get()
            if isinstance(update, Trade):
                await queue.put(update)
            elif isinstance(update, OrderBookUpdates):
                if update.update_id > order_book.update_id:
                    await queue.put(update)
