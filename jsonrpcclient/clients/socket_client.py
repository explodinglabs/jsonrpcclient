"""
Low-level socket client.
"""
import socket
from typing import Any

from ..client import Client
from ..response import Response


class SocketClient(Client):
    """
    Args:
        socket: Connected socket.
        *args: Passed through to Client class.
        **kwargs: Passed through to Client class.
    """

    def __init__(
        self, socket: socket.socket, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.socket = socket

    def send_message(self, request: str, **kwargs: Any) -> Response:
        """
        Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response (a string for requests, None for notifications).
        """
        payload = str(request) + '\n'
        self.socket.send(payload.encode())
        return Response(self.socket.recv().decode())
