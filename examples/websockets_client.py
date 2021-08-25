import asyncio
import logging

from jsonrpcclient import Ok, parse_json, request_json
import websockets


async def main():
    async with websockets.connect("ws://localhost:5000") as ws:
        await ws.send(request_json("ping"))
        response = parse_json(await ws.recv())

    if isinstance(response, Ok):
        print(response.result)
    else:
        logging.error(response.message)


asyncio.get_event_loop().run_until_complete(main())
