import json
import ssl
from typing import List, Optional

import aiohttp
import certifi


class BinanceStream:
    def __init__(self, url: str):
        self.url = url
        self._session: Optional[aiohttp.ClientSession] = None
        self._is_closing = False

    async def listen(self, subscriptions: List[str]):
        self._is_closing = False
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
