"""server.py"""

import json
import pkgutil
import logging
from abc import ABCMeta, abstractmethod

import jsonschema
from future.utils import with_metaclass

from . import exceptions
from .rpc import rpc_request_str


json_validator = jsonschema.Draft4Validator(json.loads(pkgutil.get_data(
    __name__, 'response-schema.json').decode('utf-8')))


class Server(with_metaclass(ABCMeta, object)):
    """Protocol-agnostic class representing the remote server. Subclasses should
    inherit and override ``send_message``."""

    # Request and response logs
    request_log = logging.getLogger(__name__+'.request')
    response_log = logging.getLogger(__name__+'.response')

    def __init__(self, endpoint):
        """Instantiate a remote server object.

        :param endpoint: The remote server address.
        """
        self.endpoint = endpoint

    def __getattr__(self, name):
        """Catch undefined methods and handle them as RPC requests. Technique is
        explained here: http://code.activestate.com/recipes/307618/
        """
        def attr_handler(*args, **kwargs):
            """Call self.request from here"""
            if kwargs.get('response', False):
                return self.request(name, *args, **kwargs)
            else:
                return self.notify(name, *args, **kwargs)
        return attr_handler

    def log_request(self, request, extra=None):
        """Log the JSON-RPC request before sending. Should be called by
        subclasses before sending.

        :param request: The JSON-RPC request string.
        :param extra: A dict of extra fields that may be logged.
        :return: None
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
        :return: None
        """
        if extra is None:
            extra = {}
        # Add the endpoint to the log entry
        extra.update({'endpoint': self.endpoint})
        # Clean up the response for logging
        response = response.replace("\n", '').replace('  ', ' ') \
                .replace('{ ', '{')
        self.response_log.info(response, extra=extra)

    def notify(self, method_name, *args, **kwargs):
        """JSON-RPC Notification. Notification means no response is expected.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: None
        """
        request = rpc_request_str(method_name, *args, **kwargs)
        return self.handle_response(self.send_message(request), False)

    def request(self, method_name, *args, **kwargs):
        """Send a JSON-RPC Request. Request means a response is expected.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        :return: The response string.
        """
        kwargs['response'] = True
        request = rpc_request_str(method_name, *args, **kwargs)
        return self.handle_response(self.send_message(request), True)

    @abstractmethod
    def send_message(self, request):
        """Send the RPC request to the server. Override this method in the
        protocol-specific subclass, and return the response.

        :param request: A JSON-RPC request, in dict format.
        :return: The response (a string for requests, None for notifications).
        """

    @staticmethod
    def handle_response(response, expected_response=False):
        """Processes the response and returns the 'result' portion if present.

        :param response: The JSON-RPC response string to process.
        :param expected_response: True if we were expecting a result
        :return: The response (a string for requests, None for notifications).
        """
        # A response was expected, but none was given
        if expected_response and not response:
            raise exceptions.ReceivedNoResponse()
        # Was a response given?
        if response:
            # Attempt to parse the response
            try:
                response_dict = json.loads(response)
            except ValueError:
                raise exceptions.ParseResponseError()
            # Unwanted response - A response was not asked for, but one was
            # given anyway. It may not be necessary to raise here.
            if not expected_response and 'result' in response_dict:
                raise exceptions.UnwantedResponse()
            # Validate the response against the Response schema (raises
            # jsonschema.ValidationError if invalid)
            json_validator.validate(response_dict)
            # If the response was "error", raise to ensure it's handled
            if 'error' in response_dict:
                raise exceptions.ReceivedErrorResponse(
                    response_dict['error'].get('code'),
                    response_dict['error'].get('message'),
                    response_dict['error'].get('data'))
            # Otherwise we must have a result to return
            return response_dict['result']
        # No response was given
        return None
