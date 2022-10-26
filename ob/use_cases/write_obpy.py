from ob.exchanges import BaseExchange
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

        # listener_queue = await exchange.init_listener(symbol=symbol)
        #
        # while True:
        #     message = await listener_queue.get()
        #     if message == ObpyCode.QUIT:
        #         break
        #     await queue.put(message)
        #     assert queue.qsize() < 200
