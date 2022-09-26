import asyncio
import logging

from jsonrpcclient import Ok, Error, parse_json, request_json
from websockets import connect  # type: ignore


async def main() -> None:
    async with connect("ws://localhost:5000") as ws:
        await ws.send(request_json("ping"))
        response = parse_json(await ws.recv())

    if isinstance(response, Ok):
        print(response.result)
    elif isinstance(response, Error):
        logging.error(response.message)


asyncio.get_event_loop().run_until_complete(main())
