import aiohttp


async def init_http_client():
    async with aiohttp.ClientSession() as session:
        yield session
