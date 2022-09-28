"""Websockets client"""
import asyncio
import logging

from websockets.client import connect
from jsonrpcclient import Ok, Error, parse_json, request_json


async def main() -> None:
    """Handle request"""
    async with connect("ws://localhost:5000") as socket:
        await socket.send(request_json("ping"))
        response = parse_json(await socket.recv())

    if isinstance(response, Ok):
        print(response.result)
    elif isinstance(response, Error):
        logging.error(response.message)


asyncio.get_event_loop().run_until_complete(main())
