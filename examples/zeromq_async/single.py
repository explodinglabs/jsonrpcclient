import asyncio
import logging
import sys

import zmq

from jsonrpcclient.clients.zeromq_async_client import ZeroMQAsyncClient


client = ZeroMQAsyncClient("tcp://localhost:5000")


async def main():
    response = await client.request("ping")
    if response.data.ok:
        print(response.data.result)
    else:
        logging.error(response.data.message)


asyncio.set_event_loop(zmq.asyncio.ZMQEventLoop())
asyncio.get_event_loop().run_until_complete(main())
