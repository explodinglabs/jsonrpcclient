"""Abstract base class for various clients."""
import colorlog  # type: ignore
import json
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

from .log import log_
from .parse import parse
from .request import Notification, Request
from .response import Response


request_log = colorlog.getLogger(__name__ + ".request")
response_log = colorlog.getLogger(__name__ + ".response")


class Client(metaclass=ABCMeta):
    """
    Protocol-agnostic base class for clients.

    Subclasses should inherit and override `send_message`.
    """

    def __init__(
        self,
        endpoint: str,
        id_generator: Iterator[Any] = None,
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
    ) -> None:
        """
        :param endpoint: Holds the server address.
        :param id_generator: 
        :param trim_log_values: Log abbreviated versions of requests and responses
        :param validate_against_schema: Validate responses against the JSON-RPC schema.
        """
        self.endpoint = endpoint
        self.id_generator = id_generator
        self.trim_log_values = trim_log_values
        self.validate_against_schema = validate_against_schema

    def log_request(
        self,
        request: str,
        fmt: str = "%(log_color)s\u27f6 %(message)s",
        trim: bool = False,
        **kwargs: Any
    ) -> None:
        """
        Log a request.

        :param request: The JSON-RPC request string.
        """
        return log_(request, request_log, "debug", fmt=fmt, trim=trim, **kwargs)

    def log_response(
        self,
        response: Response,
        fmt: str = "%(asctime)s %(levelname)s \u27f5 %(message)s",
        trim: bool = False,
        **kwargs: Any
    ) -> None:
        """
        Log a response.

        Note this is different to log_request, in that it takes a Response object, not a
        string.

        :param response: Response object.
        """
        return log_(response.text, response_log, "debug", fmt=fmt, trim=trim, **kwargs)

    @abstractmethod
    def send_message(self, request: str, **kwargs: Any) -> Response:
        """
        Transport the request to the server.

        Override this method in the protocol-specific subclasses.

        :param request: A JSON-RPC request.
        :returns: Response object.
        """

    def validate_response(self, response: Response) -> None:
        """
        Can be overridden for custom validation of the response.

        Raise an exception to fail validation.
        """
        pass

    def send(
        self,
        request: Union[str, Dict, List],
        trim_log_values: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        """
        Send a request, passing the whole JSON-RPC request object.

        After sending, logs, validates and parses.

        >>> client.send('{"jsonrpc": "2.0", "method": "ping", "id": 1}')
        --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
        <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}

        :param request: The JSON-RPC request.
        :type request: Either a JSON-encoded string or a Request/Notification object.
        :param kwargs: Clients can use these to configure an single request (separate to
            configuration of the whole session). For example, HTTPClient passes them on
            to `requests.Session.send()`.
        :returns: A Response object, (or ``None`` in the case of a Notification).
        :rtype: A `JSON-decoded object
            <https://docs.python.org/library/json.html#json-to-py-table>`_, or NoneType
            in the case of a Notification.
        """
        if trim_log_values is None:
            trim_log_values = self.trim_log_values
        # Convert to string
        if isinstance(request, str):
            request_text = request
        else:
            request_text = json.dumps(request)
        self.log_request(request_text, trim=trim_log_values)
        response = self.send_message(request_text, **kwargs)
        self.log_response(response, trim=trim_log_values)
        self.validate_response(response)
        response.data = parse(
            response.text, validate_against_schema=self.validate_against_schema
        )
        return response

    def notify(
        self,
        method_name: str,
        *args: Any,
        trim_log_values: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        """
        Send a JSON-RPC request, without expecting a response.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        if trim_log_values is None:
            trim_log_values = self.trim_log_values
        return self.send(
            Notification(method_name, *args, **kwargs), trim_log_values=trim_log_values
        )

    def request(
        self,
        method_name: str,
        *args: Any,
        trim_log_values: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        """
        Send a request by passing the method and arguments.

        >>> client.request('cat', name='Mittens')
        --> {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 1}
        <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
        'meow'

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        if trim_log_values is None:
            trim_log_values = self.trim_log_values
        return self.send(
            Request(method_name, *args, id_generator=self.id_generator, **kwargs),
            trim_log_values=trim_log_values,
        )

    def __getattr__(self, name: str) -> Callable:
        """
        This gives us an alternate way to make a request::

            >>> client.cube(3)
            27

        That's the same as saying ``client.request("cube", 3)``.
        """

        def attr_handler(*args: Any, **kwargs: Any) -> Response:
            """Call self.request from here"""
            return self.request(name, *args, **kwargs)

        return attr_handler
