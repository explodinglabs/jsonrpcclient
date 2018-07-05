"""Abstract base class for various clients."""
import json
import logging
import pkgutil
from abc import ABCMeta, abstractmethod
from past.builtins import basestring

from future.utils import with_metaclass
import jsonschema

from . import exceptions, ids
from .log import log_
from .prepared_request import PreparedRequest
from .request import Notification, Request


class Client(with_metaclass(ABCMeta, object)):
    """
    Protocol-agnostic base class for clients.

    Subclasses should inherit and override ``send_message``.

    :param endpoint: The server address.
    """

    # Request and response logs
    request_log = logging.getLogger(__name__ + ".request")
    response_log = logging.getLogger(__name__ + ".response")

    #: Validate the response message
    validator = jsonschema.Draft4Validator(
        json.loads(pkgutil.get_data(__name__, "response-schema.json").decode("utf-8"))
    )

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

    def log_(self, message, extra, log, level, fmt, trim):
        """Log a request or response"""
        if extra is None:
            extra = {}
        # Add the endpoint to the log entry
        extra.update({"endpoint": self.endpoint})
        # Clean up the message for logging
        if isinstance(message, basestring):
            message = message.replace("\n", "").replace("  ", " ").replace("{ ", "{")
        log_(log, level, message, extra=extra, fmt=fmt, trim=trim)

    def log_request(self, request, extra=None, fmt=None, trim=False):
        """
        Log a request.

        Should be called by subclasses in :meth:`send_message`, before sending.

        :param request: The JSON-RPC request string.
        :param extra: A dict of extra fields that may be logged.
        """
        if not fmt:
            fmt = "--> %(message)s"
        self.log_(request, extra, self.request_log, "info", fmt, trim)

    def log_response(self, response, extra=None, fmt=None, trim=False):
        """
        Log a response.

        Should be called by subclasses in :meth:`send_message`, after receiving
        the response.

        :param response: The JSON-RPC response string.
        :param extra: A dict of extra fields that may be logged.
        """
        if not fmt:
            fmt = "<-- %(message)s"
        self.log_(response, extra, self.response_log, "info", fmt, trim)

    def prepare_request(self, request, **kwargs):
        """
        Prepare the request if necessary.

        Subclasses can overload to modify the request, or to add extra info to
        the log entry (set the extra attribute).
        """
        pass

    def process_response(self, response, log_extra=None, log_format=None):
        """
        Process the response and return the 'result' portion if present.

        :param response: The JSON-RPC response string to process.
        :return: The response string, or None
        """
        if response:
            # Log the response before processing it
            self.log_response(
                response, log_extra, log_format, trim=self.trim_log_values
            )
            # If it's a json string, parse to object
            if isinstance(response, basestring):
                try:
                    response = json.loads(response)
                except ValueError:
                    raise exceptions.ParseResponseError()
            # Validate the response against the Response schema (raises
            # jsonschema.ValidationError if invalid)
            if self.validate_against_schema:
                self.validator.validate(response)
            if isinstance(response, list):
                # Batch request - just return the whole response
                return response
            else:
                # If the response was "error", raise to ensure it's handled
                if "error" in response and response["error"] is not None:
                    raise exceptions.ReceivedErrorResponseError(
                        response["error"].get("code"),
                        response["error"].get("message"),
                        response["error"].get("data"),
                    )
                # All was successful, return just the result part
                return response.get("result")
        # No response was given
        return None

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

    def send(self, request, **kwargs):
        """
        Send a request, passing the whole JSON-RPC request object.

            >>> client.send('{"jsonrpc": "2.0", "method": "ping", "id": 1}')
            --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
            <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
            'pong'

        :param request: The JSON-RPC request.
        :type request: JSON-encoded string or JSON serializable object
        :param kwargs: Clients can use these to configure an single request
            (separate to configuration of the whole session). For example,
            HTTPClient passes them on to `requests.Session.send()
            <http://docs.python-requests.org/en/master/api/#requests.Session.send>`_.
        :returns: The payload, i.e. the ``result`` part of the response, (or
            ``None`` in the case of a Notification).
        :rtype: A `JSON-decoded object
            <https://docs.python.org/library/json.html#json-to-py-table>`_.
        :raises ParseResponseError:
            The response was not valid JSON.
        :raises ValidationError:
            The response was valid JSON, but not a valid JSON-RPC response
            object.
        :raises ReceivedErrorResponseError:
            The server responded with a JSON-RPC `error object
            <http://www.jsonrpc.org/specification#error_object>`_.
        """
        # Put the raw request into an object which can be passed around the
        # subsequent method calls. Converts the request to a string not already.
        request = PreparedRequest(request)
        # Prepare request, subclasses can override to prepare the request, and
        # set the extra details to include in the log entry
        self.prepare_request(request)
        # Log the request
        self.log_request(
            request, request.log_extra, request.log_format, trim=self.trim_log_values
        )
        # Call abstract method to transport the message, returning either the
        # processed response, or a future which promises to process eventually
        return self.send_message(request, **kwargs)

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

        That's the same as saying ``client.request('cube', 3)``.
        """

        def attr_handler(*args, **kwargs):
            """Call self.request from here"""
            return self.request(name, *args, **kwargs)

        return attr_handler
