import asyncio
import aiohttp
from jsonrpcclient.clients.aiohttp_client import AiohttpClient


async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        client = AiohttpClient(session, "http://localhost:5000")
        response = await client.request("ping")
    print(response.data.result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
