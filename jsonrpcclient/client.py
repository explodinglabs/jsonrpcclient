"""
Client class.

Base class for the clients.
"""
import logging
from abc import ABCMeta, abstractmethod
from json import dumps as serialize
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

from apply_defaults import apply_config, apply_self  # type: ignore

from .config import config
from .exceptions import ReceivedErrorResponseError
from .log import log_
from .parse import parse
from .request import Notification, Request
from .response import Response

request_log = logging.getLogger(__name__ + ".request")
response_log = logging.getLogger(__name__ + ".response")


def is_batch_request(request_text: str) -> bool:
    try:
        return request_text.strip()[0] == "["
    except IndexError:
        return False


class Client(metaclass=ABCMeta):
    """
    Protocol-agnostic base class for clients.

    Subclasses must override `send_message` to transport the message.
    """

    DEFAULT_REQUEST_LOG_FORMAT = "--> %(message)s"
    DEFAULT_RESPONSE_LOG_FORMAT = "<-- %(message)s"

    @apply_config(config, converters={"id_generator": "getcallable"})
    def __init__(
        self,
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
        id_generator: Optional[Iterator] = None,
        basic_logging: bool = False,
    ) -> None:
        """
        Args:
            trim_log_values: Abbreviate the log entries of requests and responses.
            validate_against_schema: Validate response against the JSON-RPC schema.
            id_generator: Iterable of values to use as the "id" part of the request.
            basic_logging: Will create log handlers to output request & response
                messages.
        """
        self.trim_log_values = trim_log_values
        self.validate_against_schema = validate_against_schema
        self.id_generator = id_generator
        if basic_logging:
            self.basic_logging()

    def basic_logging(self) -> None:
        """
        Call this on the client object to create log handlers to output request and
        response messages.
        """
        # Request handler
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt=self.DEFAULT_REQUEST_LOG_FORMAT))
        request_log.addHandler(handler)
        request_log.setLevel(logging.INFO)
        # Response handler
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt=self.DEFAULT_RESPONSE_LOG_FORMAT))
        response_log.addHandler(handler)
        response_log.setLevel(logging.INFO)

    @apply_self
    def log_request(
        self, request: str, trim_log_values: bool = False, **kwargs: Any
    ) -> None:
        """
        Log a request.

        Args:
            request: The JSON-RPC request string.
            trim_log_values: Log an abbreviated version of the request.
        """
        return log_(request, request_log, "info", trim=trim_log_values, **kwargs)

    @apply_self
    def log_response(
        self, response: Response, trim_log_values: bool = False, **kwargs: Any
    ) -> None:
        """
        Log a response.

        Note this is different to log_request, in that it takes a Response object, not a
        string.

        Args:
            response: The Response object to log. Note this is different to log_request
                which takes a string.
            trim_log_values: Log an abbreviated version of the response.
        """
        return log_(response.text, response_log, "info", trim=trim_log_values, **kwargs)

    @abstractmethod
    def send_message(self, request: str, **kwargs: Any) -> Response:
        """
        Transport the request to the server.

        Override this method in the protocol-specific subclasses.

        Args:
            request: A JSON-RPC request.
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
        <Response[1]>

        Args:
            request: The JSON-RPC request. Can be either a JSON-encoded string or a
                Request/Notification object.
            trim_log_values: Abbreviate the log entries of requests and responses.
            validate_against_schema: Validate response against the JSON-RPC schema.
            kwargs: Clients can use this to configure an single request. For example,
                HTTPClient passes this through to `requests.Session.send()`.
            in the case of a Notification.
        """
        # Convert the request to a string if it's not already.
        request_text = request if isinstance(request, str) else serialize(request)
        batch = is_batch_request(request_text)
        self.log_request(request_text, trim_log_values=trim_log_values)
        response = self.send_message(request_text, **kwargs)
        self.log_response(response, trim_log_values=trim_log_values)
        self.validate_response(response)
        response.data = parse(
            response.text, batch=batch, validate_against_schema=validate_against_schema
        )
        if not isinstance(response.data, list) and not response.data.ok:
            raise ReceivedErrorResponseError(response)
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

        Args:
            method_name: The remote procedure's method name.
            args: Positional arguments passed to the remote procedure.
            kwargs: Keyword arguments passed to the remote procedure.
            trim_log_values: Abbreviate the log entries of requests and responses.
            validate_against_schema: Validate response against the JSON-RPC schema.
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

        >>> client.request("cat", name="Yoko")
        <Response[1]

        Args:
            method_name: The remote procedure's method name.
            args: Positional arguments passed to the remote procedure.
            kwargs: Keyword arguments passed to the remote procedure.
            trim_log_values: Abbreviate the log entries of requests and responses.
            validate_against_schema: Validate response against the JSON-RPC schema.
            id_generator: Iterable of values to use as the "id" part of the request.
        """
        return self.send(
            Request(method_name, id_generator=id_generator, *args, **kwargs),
            trim_log_values=trim_log_values,
            validate_against_schema=validate_against_schema,
        )

    def __getattr__(self, name: str) -> Callable:
        """
        This gives us an alternate way to make a request.

        >>> client.cube(3)
        --> {"jsonrpc": "2.0", "method": "cube", "params": [3], "id": 1}

        That's the same as saying `client.request("cube", 3)`.
        """

        def attr_handler(*args: Any, **kwargs: Any) -> Response:
            return self.request(name, *args, **kwargs)

        return attr_handler
