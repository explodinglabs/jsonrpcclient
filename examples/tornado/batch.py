import logging

from tornado.ioloop import IOLoop

from jsonrpcclient.clients.tornado_client import TornadoClient
from jsonrpcclient.requests import Request

client = TornadoClient("http://localhost:5000/")


async def main():
    response = await client.send([Request("ping"), Request("ping"), Request("ping")])
    for data in response.data:
        if data.ok:
            print("{}: {}".format(data.id, data.result))
        else:
            logging.error("%d: %s", data.id, data.message)


IOLoop.current().run_sync(main)
