import asyncio
import logging

import aiohttp

from jsonrpcclient.clients.aiohttp_client import AiohttpClient
from jsonrpcclient.request import Request


async def main(loop):

    async with aiohttp.ClientSession(loop=loop) as session:
        client = AiohttpClient(session, "http://localhost:5000")
        requests = [Request("ping"), Request("ping"), Request("ping")]
        response = await client.send(requests)

    for data in response.data:
        if data.ok:
            print("{}: {}".format(data.id, data.result))
        else:
            logging.error("%d: %s", data.id, data.message)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
