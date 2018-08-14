"""Abstract base class for various clients."""
import json
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

import colorlog  # type: ignore
from apply_defaults import apply_self, apply_config

from .config import config
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

    @apply_config(config, converters={"id_generator": "getcallable"})
    def __init__(
        self,
        endpoint: str,
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
        id_generator: Optional[Iterator] = None,
    ) -> None:
        """
        :param endpoint: Holds the server address.
        :param config: Log abbreviated versions of requests and responses.
        """
        self.endpoint = endpoint
        self.trim_log_values = trim_log_values
        self.validate_against_schema = validate_against_schema
        self.id_generator = id_generator

    @apply_self
    def log_request(
        self,
        request: str,
        fmt: str = "%(log_color)s\u27f6 %(message)s",
        trim_log_values: bool = False,
        **kwargs: Any
    ) -> None:
        """
        Log a request.

        :param request: The JSON-RPC request string.
        """
        return log_(
            request, request_log, "debug", fmt=fmt, trim=trim_log_values, **kwargs
        )

    @apply_self
    def log_response(
        self,
        response: Response,
        fmt: str = "%(asctime)s %(levelname)s \u27f5 %(message)s",
        trim_log_values: bool = False,
        **kwargs: Any
    ) -> None:
        """
        Log a response.

        Note this is different to log_request, in that it takes a Response object, not a
        string.

        :param response: Response object.
        """
        return log_(
            response.text,
            response_log,
            "debug",
            fmt=fmt,
            trim=trim_log_values,
            **kwargs
        )

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

    @apply_self
    def send(
        self,
        request: Union[str, Dict, List],
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
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
        # Convert to string
        request_text = request if isinstance(request, str) else json.dumps(request)
        self.log_request(request_text, trim_log_values=trim_log_values)
        response = self.send_message(request_text, **kwargs)
        self.log_response(response, trim_log_values=trim_log_values)
        self.validate_response(response)
        response.data = parse(
            response.text, validate_against_schema=validate_against_schema
        )
        return response

    @apply_self
    def notify(
        self,
        method_name: str,
        *args: Any,
        trim_log_values: Optional[bool] = None,
        validate_against_schema: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        """
        Send a JSON-RPC request, without expecting a response.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        return self.send(
            Notification(method_name, *args, **kwargs),
            trim_log_values=trim_log_values,
            validate_against_schema=validate_against_schema,
        )

    @apply_self
    def request(
        self,
        method_name: str,
        *args: Any,
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
        id_generator: Optional[Iterator] = None,
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
        return self.send(
            Request(method_name, id_generator=id_generator, *args, **kwargs),
            trim_log_values=trim_log_values,
            validate_against_schema=validate_against_schema,
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
