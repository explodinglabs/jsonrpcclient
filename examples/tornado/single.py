import logging
from tornado.ioloop import IOLoop
from jsonrpcclient.clients.tornado_client import TornadoClient

client = TornadoClient("http://localhost:5000/")

async def main():
    response = await client.request("ping")
    if response.data.ok:
        print(response.data.result)
    else:
        logging.error(response.data.message)

IOLoop.current().run_sync(main)
