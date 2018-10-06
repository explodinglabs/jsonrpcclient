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
        Args:
            socket: Connected websocket (websockets.connect("ws://localhost:5000"))
        """
        super().__init__(*args, **kwargs)
        self.socket = socket

    async def send_message(
        self, request: str, response_expected: bool, **kwargs: Any
    ) -> Response:
        """
        Transport the message to the server and return the response.

        Args:
            request: The JSON-RPC request string.
            response_expected: Whether the request expects a response.

        Returns:
            A Response object.
        """
        await self.socket.send(request)
        if response_expected:
            response_text = await self.socket.recv()
            return Response(response_text)
        return Response("")
