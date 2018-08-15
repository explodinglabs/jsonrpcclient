import asyncio

import zmq

from jsonrpcclient.clients.zeromq_async_client import ZeroMQAsyncClient


async def main():
    client = ZeroMQAsyncClient('tcp://localhost:5000')
    response = await client.request('ping')
    print(response)

asyncio.set_event_loop(zmq.asyncio.ZMQEventLoop())
asyncio.get_event_loop().run_until_complete(main())
