import asyncio
import os

from ob.exchanges import BaseExchange
from ob.models import ObpyCode, Symbol


class WriteObpy:
    def __init__(self, exchange: BaseExchange, file_path: str, symbol: Symbol):
        self.exchange = exchange
        self.file_path = file_path
        self.symbol = symbol

    async def call(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        queue = asyncio.Queue()
        asyncio.ensure_future(self.exchange.listen(symbol=self.symbol, queue=queue))

        with open(self.file_path, "w") as f:
            f.write(self.exchange.to_line() + "\n")
            f.write(self.symbol.to_line() + "\n")

            while True:
                message = await queue.get()
                if message == ObpyCode.QUIT:
                    break
                f.write(message.to_line() + "\n")
                assert queue.qsize() < 200
