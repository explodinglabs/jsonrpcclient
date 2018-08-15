"""
Websockets client.

http://websockets.readthedocs.io/
"""
from typing import Any

from websockets import WebSocketCommonProtocol  # type: ignore

from ..async_client import AsyncClient
from ..response import Response


class WebSocketsClient(AsyncClient):
    def __init__(
        self, socket: WebSocketCommonProtocol, *args: Any, **kwargs: Any
    ) -> None:
        """
        :param socket: Connected websocket (websockets.connect("ws://localhost:5000"))
        :param *args: Passed through to Client class.
        :param **kwargs: Passed through to Client class.
        """
        super().__init__(*args, **kwargs)
        self.socket = socket

    async def send_message(self, request: str, **kwargs: Any):  # type: ignore
        await self.socket.send(request)
        response_text = await self.socket.recv()
        return Response(response_text)
