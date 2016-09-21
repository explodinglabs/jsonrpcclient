from tornado.ioloop import IOLoop
from jsonrpcclient.tornado_client import TornadoClient

client = TornadoClient('http://localhost:5000/')

async def main():
    print(await client.request('ping'))

IOLoop.current().run_sync(main)
