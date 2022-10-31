import asyncio

from ob.exchanges import BaseExchange
from ob.factories import ObpyFileFactory
from ob.models import ObpyCode, ObpyFile, Symbol


class WriteObpy:
    def __init__(
        self, exchange: BaseExchange, obpy_file_factory: ObpyFileFactory, symbol: Symbol
    ):
        self.exchange = exchange
        self.obpy_file_factory = obpy_file_factory
        self.symbol = symbol

    async def call(self) -> ObpyFile:
        queue = asyncio.Queue()
        asyncio.ensure_future(self.exchange.listen(symbol=self.symbol, queue=queue))

        ts_start = 0
        ts_stop = 0

        obpy_file = self.obpy_file_factory.from_symbol(
            exchange_slug=self.exchange.slug, symbol_slug=self.symbol.slug
        )

        try:
            with open(obpy_file.temp_path, "w") as f:
                f.write(self.exchange.to_line() + "\n")
                f.write(self.symbol.to_line() + "\n")

                while True:
                    message = await queue.get()
                    if message == ObpyCode.QUIT:
                        break
                    f.write(message.to_line() + "\n")

                    ts_start = ts_start or message.ts
                    ts_stop = message.ts or ts_stop

                    assert queue.qsize() < 200
        except Exception:
            pass
        finally:
            obpy_file.finalize(ts_start, ts_stop)

        return obpy_file
