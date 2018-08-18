"""
ZeroMQ client.

ZMQClient('tcp://hostname:5555').request('go')
"""
from typing import Any

import zmq  # type: ignore

from ..client import Client
from ..response import Response


class ZeroMQClient(Client):
    """
    Args:
        endpoint: The server address.
        socket_type: The zeromq `socket type`_. Default is `zmq.REQ`.
        *args: Passed through to Client class.
        **kwargs: Passed through to Client class.
    """

    def __init__(
        self, endpoint: str, *args: Any, socket_type: int = zmq.REQ, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    def send_message(self, request: str, **kwargs: Any) -> Response:
        """
        Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response (a string for requests, None for notifications).
        """
        self.socket.send_string(request)
        return Response(self.socket.recv().decode())
