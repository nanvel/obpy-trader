import asyncio
import certifi
import json
import ssl
import logging
from typing import List, Optional

import aiohttp


OB_URL = "https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=5000"


class ExchangeStream:

    EXCHANGE_SOCKET_URL = "wss://stream.binance.com:9443/stream"

    def __init__(self, url):
        self.url = url
        self._session: Optional[aiohttp.ClientSession] = None
        self._is_closing = False

    async def listen(self, subscriptions: List[str]):
        self._session = aiohttp.ClientSession()
        try:
            ws = await self._session.ws_connect(
                self.url,
                heartbeat=50,
                ssl=ssl.create_default_context(cafile=certifi.where()),
            )

            for n, subscription in enumerate(subscriptions):
                await ws.send_json(
                    {
                        "method": "SUBSCRIBE",
                        "id": n,
                        "params": subscriptions,
                    }
                )

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    yield data
                assert msg.type != aiohttp.WSMsgType.closed
        except Exception:
            pass
        finally:
            if not self._session.closed:
                await self._session.close()

    async def close(self):
        self._is_closing = True
        if self._session is not None and not self._session.closed:
            await self._session.close()


async def listener(symbol: str, queue: asyncio.Queue):
    stream = ExchangeStream()
    async for row in stream.listen(
        subscriptions=[f"{symbol.lower()}@depth@100ms", f"{symbol.lower()}@aggTrade"]
    ):
        await queue.put(row)


async def main():
    queue = asyncio.Queue()

    # asyncio.ensure_future(listener(symbol="BTCUSDT", queue=queue))
    #
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(OB_URL) as response:
    #         ob_initial = await response.json()
    #
    # while True:
    #     res = await queue.get()
    #     print(res)

    # print(ob_initial)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.binance.com/api/v3/exchangeInfo?symbol=BTCUSDT"
        ) as response:
            symbol_info = await response.json()

    print(json.dumps(symbol_info, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
