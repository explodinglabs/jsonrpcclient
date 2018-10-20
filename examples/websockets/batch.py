import asyncio
import logging

import websockets

from jsonrpcclient.clients.websockets_client import WebSocketsClient
from jsonrpcclient.requests import Request, Notification


async def main():

    async with websockets.connect("ws://localhost:5000") as ws:
        requests = [Request("ping"), Notification("ping"), Request("ping")]
        response = await WebSocketsClient(ws).send(requests)

    for data in response.data:
        if data.ok:
            print("{}: {}".format(data.id, data.result))
        else:
            logging.error("%d: %s", data.id, data.message)


asyncio.get_event_loop().run_until_complete(main())
