"""Abstract base class for various clients."""
import json
import logging
from abc import ABCMeta, abstractmethod


from . import exceptions
from .log import log_
from .request import Notification, Request
from .response import Response


request_log = logging.getLogger(__name__ + ".request")
response_log = logging.getLogger(__name__ + ".response")


class Client(metaclass=ABCMeta):
    """
    Protocol-agnostic base class for clients.

    Subclasses should inherit and override ``send_message``.

    :param endpoint: The server address.
    """

    def __init__(
        self,
        endpoint,
        id_generator=None,
        trim_log_values=False,
        validate_against_schema=True,
    ):
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

    def log_request(self, request, fmt="--> %(message)s", trim=None, **kwargs):
        """
        Log a request.

        :param request: The JSON-RPC request string.
        """
        trim = trim or self.trim_log_values
        return log_(request, request_log, fmt=fmt, trim=trim, **kwargs)

    def log_response(self, response, fmt="<-- %(message)s", trim=None, **kwargs):
        """
        Log a response.

        Note this is different to log_request, in that it takes a Response object, not a
        string.

        :param response: Response object.
        """
        trim = trim or self.trim_log_values
        return log_(response.text, response_log, fmt=fmt, trim=trim, **kwargs)

    @abstractmethod
    def send_message(self, request, **kwargs):
        """
        Transport the request to the server.

        Override this method in the protocol-specific subclasses.

        :param request: A JSON-RPC request, in dict format.
        :returns: The processed response - for requests, it will be the result
        part of the response, None for notifications, or an entire jsonrpc
        response for batch requests.
        """

    def validate_response(self, response):
        """Can be overridden to validate the response"""
        pass

    def send(self, request, **kwargs):
        """
        Send a request, passing the whole JSON-RPC request object.

        >>> client.send('{"jsonrpc": "2.0", "method": "ping", "id": 1}')
        --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
        <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
        'pong'

        Also logs and validates

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
        if isinstance(request, Notification):  # Includes Requests
            request = str(request)
        elif not isinstance(request, str):
            request = json.dumps(request)
        self.log_request(request)
        response = self.send_message(request, **kwargs)
        self.log_response(response)
        self.validate_response(response)
        response.parse(validate_against_schema=self.validate_against_schema)
        return response

    def notify(self, method_name, *args, **kwargs):
        """
        Send a JSON-RPC request, without expecting a response.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        return self.send(Notification(method_name, *args, **kwargs))

    def request(self, method_name, *args, **kwargs):
        """
        Send a request by passing the method and arguments.

        This is the main public method.

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
            Request(method_name, *args, id_generator=self.id_generator, **kwargs)
        )

    def __getattr__(self, name):
        """
        This gives us an alternate way to make a request::

            >>> client.cube(3)
            27

        That's the same as saying ``client.request("cube", 3)``.
        """

        def attr_handler(*args, **kwargs):
            """Call self.request from here"""
            return self.request(name, *args, **kwargs)

        return attr_handler
