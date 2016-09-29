import asyncio
import zmq
from jsonrpcclient.zeromq_async_client import ZeroMQAsyncClient

async def main():
    response = await ZeroMQAsyncClient('tcp://localhost:5000').request('ping')
    print(response)

asyncio.set_event_loop(zmq.asyncio.ZMQEventLoop())
asyncio.get_event_loop().run_until_complete(main())
