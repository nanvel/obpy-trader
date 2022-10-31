import asyncio

from ob.exchanges import BaseExchange
from ob.models import ObpyCode, ObpyFile, Symbol


class WriteObpy:
    def __init__(self, exchange: BaseExchange, obpy_file: ObpyFile, symbol: Symbol):
        self.exchange = exchange
        self.obpy_file = obpy_file
        self.symbol = symbol

    async def call(self):
        queue = asyncio.Queue()
        asyncio.ensure_future(self.exchange.listen(symbol=self.symbol, queue=queue))

        with open(self.obpy_file.temp_path, "w") as f:
            f.write(self.exchange.to_line() + "\n")
            f.write(self.symbol.to_line() + "\n")

            while True:
                message = await queue.get()
                if message == ObpyCode.QUIT:
                    break
                f.write(message.to_line() + "\n")

                self.obpy_file.update_ts(message.ts)

                assert queue.qsize() < 200
