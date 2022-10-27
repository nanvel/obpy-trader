from asyncio import Queue

from ob.exchanges import BaseExchange
from ob.models import ObpyCode
from ob.storage import BaseWriter


class WriteObpy:
    def __init__(self, exchange: BaseExchange, writer: BaseWriter, symbol_slug: str):
        self.exchange = exchange
        self.writer = writer
        self.symbol_slug = symbol_slug

    async def call(self):
        symbol = await self.exchange.pull_symbol(symbol_slug=self.symbol_slug)

        await self.writer.write(
            lines=[
                self.exchange.to_line(),
                symbol.to_line(),
            ]
        )

        queue = Queue()

        listener_task = await self.exchange.init_listener(symbol=symbol, queue=queue)

        while True:
            message = await queue.get()
            if message == ObpyCode.QUIT:
                break
            await self.writer.write(lines=[message.to_line()])
            assert queue.qsize() < 200
