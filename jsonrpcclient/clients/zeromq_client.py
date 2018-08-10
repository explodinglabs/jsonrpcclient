"""
ZeroMQ Client
*************

A ZeroMQ client to send requests::

    ZMQClient('tcp://hostname:5555').request('go')
"""
import zmq  # type: ignore
from typing import Any

from ..client import Client
from ..response import Response


class ZeroMQClient(Client):
    """
    :param endpoint: The server address.
    :param socket_type: The zeromq `socket type`_. Default is *zmq.REQ*.
    :param *args: Passed through to Client class.
    :param **kwargs: Passed through to Client class.
    """

    def __init__(
        self, endpoint: str, *args: Any, socket_type: int = zmq.REQ, **kwargs: Any
    ) -> None:
        super().__init__(endpoint, *args, **kwargs)
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
