import asyncio
import logging

import aiohttp

from jsonrpcclient.clients.aiohttp_client import AiohttpClient


async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        client = AiohttpClient(session, "http://localhost:5000")
        response = await client.request("ping")
    if response.data.ok:
        print(response.data.result)
    else:
        logging.error(response.data.message)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
