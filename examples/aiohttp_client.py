"""Aiohttp client"""
import asyncio
import logging

from aiohttp import ClientSession
from jsonrpcclient import Ok, Error, request, parse


async def main() -> None:
    """Handle async request"""
    async with ClientSession() as session:
        async with session.post(
            "http://localhost:5000", json=request("ping")
        ) as response:
            parsed = parse(await response.json())
            if isinstance(parsed, Ok):
                print(parsed.result)
            elif isinstance(parse, Error):
                logging.error(parsed.message)


asyncio.get_event_loop().run_until_complete(main())
