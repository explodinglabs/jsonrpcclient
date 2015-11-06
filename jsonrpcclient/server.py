"""
Server
******
"""

import json
import pkgutil
import logging
from abc import ABCMeta, abstractmethod
from past.builtins import basestring

import jsonschema
from future.utils import with_metaclass

from jsonrpcclient import exceptions
from jsonrpcclient.request import Notification, Request


class Server(with_metaclass(ABCMeta, object)):
    """Protocol-agnostic class representing the remote server. Subclasses should
    inherit and override ``send_message``.

    :param endpoint: The server address.
    """

    # Request and response logs
    request_log = logging.getLogger(__name__+'.request')
    response_log = logging.getLogger(__name__+'.response')

    #: Validator
    validator = jsonschema.Draft4Validator(json.loads(pkgutil.get_data(
        __name__, 'response-schema.json').decode('utf-8')))

    def __init__(self, endpoint):
        #: Holds the server address
        self.endpoint = endpoint

    def log_request(self, request, extra=None):
        """Log the JSON-RPC request before sending. Should be called by
        subclasses before sending.

        :param request: The JSON-RPC request string.
        :param extra: A dict of extra fields that may be logged.
        """
        if extra is None:
            extra = {}
        # Add endpoint to list of info to include in log message
        extra.update({'endpoint': self.endpoint})
        self.request_log.info(request, extra=extra)

    def log_response(self, response, extra=None):
        """Log the JSON-RPC response after sending. Should be called by
        subclasses after sending.

        :param response: The JSON-RPC response string.
        :param extra: A dict of extra fields that may be logged.
        """
        if extra is None:
            extra = {}
        # Add the endpoint to the log entry
        extra.update({'endpoint': self.endpoint})
        # Clean up the response for logging
        response = response.replace("\n", '').replace('  ', ' ') \
                .replace('{ ', '{')
        self.response_log.info(response, extra=extra)

    def _process_response(self, response):
        """Processes the response and returns the 'result' portion if present.

        :param response: The JSON-RPC response string to process.
        :return: The response string, or None
        :raise jsonschema.ValidationError:
        :raise jsonrpcclient.JsonRpcClientError:
        """
        if response:
            if isinstance(response, basestring):
                # Attempt to parse the response
                try:
                    response = json.loads(response)
                except ValueError:
                    raise exceptions.ParseResponseError()
            # Validate the response against the Response schema (raises
            # jsonschema.ValidationError if invalid)
            if self.validator:
                self.validator.validate(response)
            if isinstance(response, list):
                # For now, just return the whole response
                return response
            else:
                # If the response was "error", raise to ensure it's handled
                if 'error' in response:
                    raise exceptions.ReceivedErrorResponse(
                        response['error'].get('code'),
                        response['error'].get('message'),
                        response['error'].get('data'))
                # else
                return response.get('result')
        # No response was given
        return None

    @abstractmethod
    def send_message(self, request):
        """Send the RPC request to the server. Override this method in the
        protocol-specific subclass, and return the response.

        :param request: A JSON-RPC request, in dict format.
        :return: The response (a string for requests, None for notifications).
        """

    def send(self, request):
        """Send a request or batch of requests."""
        response = self.send_message(str(request))
        return self._process_response(response)

    # Alternate ways to send a request -----------

    def notify(self, method_name, *args, **kwargs):
        """Send a JSON-RPC request, without expecting a response.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response.)
        """
        return self.send(Notification(method_name, *args, **kwargs))

    def request(self, method_name, *args, **kwargs):
        """Send a JSON-RPC request, and get a response.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The payload (i.e. the ``result`` part of the response.)
        """
        return self.send(Request(method_name, *args, **kwargs))

    def __getattr__(self, name):
        """This gives us an alternate way to make a request::

            >>> server.cube(3)
            27

        That's the same as saying ``server.request('cube', 3)``.

        Technique is explained here: http://code.activestate.com/recipes/307618/
        """
        def attr_handler(*args, **kwargs):
            """Call self.request from here"""
            return self.request(name, *args, **kwargs)
        return attr_handler
