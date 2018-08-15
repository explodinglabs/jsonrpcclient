import asyncio
import logging
import sys

import zmq

from jsonrpcclient.clients.zeromq_async_client import ZeroMQAsyncClient
from jsonrpcclient.request import Request


client = ZeroMQAsyncClient("tcp://127.0.0.1:5000")


async def main():
    response = await client.send([Request("ping"), Request("ping"), Request("ping")])
    for data in response.data:
        if data.ok:
            print("{}: {}".format(data.id, data.result))
        else:
            logging.error("%d: %s", data.id, data.message)


asyncio.get_event_loop().run_until_complete(main())
