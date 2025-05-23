# Examples

## aiohttp

```python
import asyncio
import logging

from aiohttp import ClientSession

from jsonrpcclient import Error, Ok, parse, request


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
```

See [blog post](https://explodinglabs.github.io/jsonrpc/aiohttp).

## Requests

```python
import logging

import requests

from jsonrpcclient import Error, Ok, parse, request

response = requests.post("http://localhost:5000/", json=request("ping"), timeout=10)
parsed = parse(response.json())
if isinstance(parsed, Ok):
    print(parsed.result)
elif isinstance(parsed, Error):
    logging.error(parsed.message)
```

## Websockets

```python
import asyncio
import logging

from websockets.client import connect

from jsonrpcclient import Error, Ok, parse_json, request_json


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
```

See [blog post](https://explodinglabs.github.io/jsonrpc/websockets).

## ZeroMQ

```python
import logging

import zmq

from jsonrpcclient import Ok, parse_json, request_json

socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5000")
socket.send_string(request_json("ping"))
response = parse_json(socket.recv().decode())
if isinstance(response, Ok):
    print(response.result)
else:
    logging.error(response.message)
```

See [blog post](https://explodinglabs.github.io/jsonrpc/zeromq).
