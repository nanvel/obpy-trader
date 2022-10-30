import asyncio
import os
import time

from ob.exchanges import BaseExchange
from ob.models import ObpyCode
from ob.storage.use_cases.build_file_path import BuildFilePath


class WriteObpy:
    def __init__(
        self, exchange: BaseExchange, build_file_path: BuildFilePath, symbol_slug: str
    ):
        self.exchange = exchange
        self.build_file_path = build_file_path
        self.symbol_slug = symbol_slug

    async def call(self):
        symbol = await self.exchange.pull_symbol(symbol_slug=self.symbol_slug)

        file_path = self.build_file_path.call(
            exchange=self.exchange.slug, symbol=symbol, ts=int(time.time())
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        queue = asyncio.Queue()
        asyncio.ensure_future(self.exchange.listen(symbol=symbol, queue=queue))

        with open(file_path, "w") as f:
            f.write(self.exchange.to_line() + "\n")
            f.write(symbol.to_line() + "\n")

            while True:
                message = await queue.get()
                if message == ObpyCode.QUIT:
                    break
                f.write(message.to_line() + "\n")
                assert queue.qsize() < 200
