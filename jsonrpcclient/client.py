"""Abstract class for various clients"""

import json
import pkgutil
import logging
from abc import ABCMeta, abstractmethod
from past.builtins import basestring #pylint:disable=redefined-builtin

import jsonschema
from future.utils import with_metaclass

from . import config, exceptions
from .request import Notification, Request
from .log import log_
from .prepared_request import PreparedRequest


class Client(with_metaclass(ABCMeta, object)):
    """Protocol-agnostic base class the clients. Subclasses should inherit and
    override ``_send_message``.

    :param endpoint: The server address.
    """

    # Request and response logs
    _request_log = logging.getLogger(__name__+'.request')
    _response_log = logging.getLogger(__name__+'.response')

    #: Validate the response message
    _validator = jsonschema.Draft4Validator(json.loads(pkgutil.get_data(
        __name__, 'response-schema.json').decode('utf-8')))

    def __init__(self, endpoint):
        #: Holds the server address
        self.endpoint = endpoint

    def log_(self, message, extra, log, level, fmt):
        """Log a request or response"""
        if extra is None:
            extra = {}
        # Add the endpoint to the log entry
        extra.update({'endpoint': self.endpoint})
        # Clean up the message for logging
        if isinstance(message, basestring):
            message = message.replace("\n", '').replace('  ', ' ') \
                .replace('{ ', '{')
        log_(log, level, message, extra=extra, fmt=fmt)

    def _log_request(self, request, extra=None, fmt=None):
        """Log the JSON-RPC request before sending. Should be called by
        subclasses in :meth:`_send_message`, before sending.

        :param request: The JSON-RPC request string.
        :param extra: A dict of extra fields that may be logged.
        """
        if not fmt:
            fmt = '--> %(message)s'
        self.log_(request, extra, self._request_log, 'info', fmt)

    def _log_response(self, response, extra=None, fmt=None):
        """Log the JSON-RPC response after sending. Should be called by
        subclasses in :meth:`_send_message`, after receiving the response.

        :param response: The JSON-RPC response string.
        :param extra: A dict of extra fields that may be logged.
        """
        if not fmt:
            fmt = '<-- %(message)s'
        self.log_(response, extra, self._response_log, 'info', fmt)

    def _prepare_request(self, request, **kwargs):
        """Prepare the request if necessary. Subclasses can overload to modify
        the request, or to add extra info to the log entry (set the
        extra attribute).
        """
        pass

    def _process_response(self, response, log_extra=None, log_format=None):
        """Processes the response and returns the 'result' portion if present.

        :param response: The JSON-RPC response string to process.
        :return: The response string, or None
        """
        if response:
            # Log the response before processing it
            self._log_response(response, log_extra, log_format)
            # If it's a json string, parse to object
            if isinstance(response, basestring):
                try:
                    response = json.loads(response)
                except ValueError:
                    raise exceptions.ParseResponseError()
            # Validate the response against the Response schema (raises
            # jsonschema.ValidationError if invalid)
            if config.validate:
                self._validator.validate(response)
            if isinstance(response, list):
                # Batch request - just return the whole response
                return response
            else:
                # If the response was "error", raise to ensure it's handled
                if 'error' in response:
                    raise exceptions.ReceivedErrorResponse(
                        response['error'].get('code'),
                        response['error'].get('message'),
                        response['error'].get('data'))
                # All was successful, return just the result part
                return response.get('result')
        # No response was given
        return None

    @abstractmethod
    def _send_message(self, request, **kwargs):
        """Transport the request to the server. Override this method in the
        protocol-specific subclasses.

        :param request: A JSON-RPC request, in dict format.
        :returns: The processed response - for requests, it will be the result
        part of the response, None for notifications, or an entire jsonrpc
        response for batch requests.
        """

    def send(self, request, **kwargs):
        """Send a request, passing the whole JSON-RPC `request object
        <http://www.jsonrpc.org/specification#request_object>`_.

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
        :raises ReceivedErrorResponse:
            The server responded with a JSON-RPC `error object
            <http://www.jsonrpc.org/specification#error_object>`_.
        """
        # Put the raw request into an object which can be passed around the
        # subsequent method calls. Converts the request to a string not already.
        request = PreparedRequest(request)
        # Prepare request, subclasses can override to prepare the request, and
        # set the extra details to include in the log entry
        self._prepare_request(request, **kwargs)
        # Log the request
        self._log_request(request, request.log_extra, request.log_format)
        # Call abstract method to transport the message, returning either the
        # processed response, or a future which promises to process eventually
        return self._send_message(request, **kwargs)

    def notify(self, method_name, *args, **kwargs):
        """Send a JSON-RPC request, without expecting a response.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        return self.send(Notification(method_name, *args, **kwargs))

    def request(self, method_name, *args, **kwargs):
        #:pylint:disable=line-too-long
        """Send a request by passing the method and arguments. This is the main
        public method.

            >>> client.request('cat', name='Mittens')
            --> {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 1}
            <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
            'meow'

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response).
        """
        #:pylint:enable=line-too-long
        return self.send(Request(method_name, *args, **kwargs))

    def __getattr__(self, name):
        """This gives us an alternate way to make a request::

            >>> client.cube(3)
            27

        That's the same as saying ``client.request('cube', 3)``.

        Technique is explained here: http://code.activestate.com/recipes/307618/
        """
        def attr_handler(*args, **kwargs):
            """Call self.request from here"""
            return self.request(name, *args, **kwargs)
        return attr_handler
