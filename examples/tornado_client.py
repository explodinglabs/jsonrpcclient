from tornado.ioloop import IOLoop
from jsonrpcclient.clients.tornado_client import TornadoClient

client = TornadoClient('http://localhost:5000/')

async def main():
    response = await client.request('ping')
    print(response)

IOLoop.current().run_sync(main)
