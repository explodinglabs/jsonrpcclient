"""ZeroMQ Client"""
from typing import Any

import zmq  # type: ignore
import zmq.asyncio  # type: ignore

from ..async_client import AsyncClient
from ..response import Response


class ZeroMQAsyncClient(AsyncClient):
    """
    :param endpoint:
    :param socket_type:
    :param **kwargs: Passed through to Client class.
    """

    def __init__(
        self, endpoint: str, *args: Any, socket_type: int = zmq.REQ, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    async def send_message(  # type: ignore
        self, request: str, **kwargs: Any
    ) -> Response:
        await self.socket.send_multipart((request.encode(),))
        response = await self.socket.recv_multipart()
        return Response(response[0].decode(), raw=response)
