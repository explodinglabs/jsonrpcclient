"""
ZeroMQ client.

ZMQClient('tcp://hostname:5555').request('go')
"""
from typing import Any

import zmq  # type: ignore

from ..client import Client
from ..response import Response


class ZeroMQClient(Client):
    def __init__(
        self, endpoint: str, *args: Any, socket_type: int = zmq.REQ, **kwargs: Any
    ) -> None:
        """
        Args:
            endpoint: The server address.
            socket_type: The zeromq socket type.
        """
        super().__init__(*args, **kwargs)
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    def send_message(
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
        self.socket.send_string(request)
        return Response(self.socket.recv().decode())
