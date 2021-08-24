import asyncio
import json
import logging

from jsonrpcclient import Ok, parse, request
import websockets


async def main():
    async with websockets.connect("ws://localhost:5000") as ws:
        await ws.send(request("ping"))
        response = parse(json.loads(await ws.recv()))

    if isinstance(response, Ok):
        print(response.result)
    else:
        logging.error(response.message)


asyncio.get_event_loop().run_until_complete(main())
