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
        encoding: The charset to encode and decode the data with.
        delimiter: String marking the end of a request or response.
        *args: Passed through to Client class.
        **kwargs: Passed through to Client class.
    """

    def __init__(
        self,
        socket: socket.socket,
        *args: Any,
        encoding: str = "utf-8",
        delimiter: str = "\n",
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.socket = socket
        self.delimiter = delimiter
        self.encoding = encoding
        self.delimiter_length = len(delimiter)

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
        payload = str(request) + self.delimiter
        self.socket.send(payload.encode(self.encoding))

        response = bytes()
        decoded = None

        # Receive the response until we find the delimiter.
        # TODO Do not wait for a response if the message sent is a notification.
        while True:
            response += self.socket.recv(1024)

            decoded = response.decode(self.encoding)
            if len(decoded) < self.delimiter_length:
                continue

            # TODO Check that're not in the middle of the response.
            elif decoded[-self.delimiter_length :] == self.delimiter:
                break

        assert decoded is not None
        return Response(decoded[: -self.delimiter_length])
