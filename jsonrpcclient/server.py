"""server.py"""

import json
import pkgutil
import logging

import jsonschema

from . import rpc, exceptions


class Server(object):
    """Transport-agnostic class representing the remote server. Should be
    inherited by transport-specific subclasses."""
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
        subclasses before transporting.

        :param request: The JSON-RPC request string.
        :param extra: A dict of extra fields that may be logged.
        """
        if hasattr(extra, 'update'):
            extra.update({'endpoint': self.endpoint})
        self.request_log.info(request, extra=extra)

    def log_response(self, response, extra=None):
        """Log the JSON-RPC response after sending. Should be called by
        subclasses after transporting.

        :param response: The JSON-RPC response string.
        :param extra: A dict of extra fields that may be logged.
        """
        response = response.replace("\n", '').replace('  ', ' ') \
                .replace('{ ', '{')
        if hasattr(extra, 'update'):
            extra.update({'endpoint': self.endpoint})
        self.response_log.info(response, extra=extra)

    def request(self, method_name, *args, **kwargs):
        """Send a JSON-RPC Request. Request means a response is expected.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        """
        kwargs['response'] = True
        return self.handle_response(
            self.send_message(rpc.request(method_name, *args, **kwargs)), True)

    def notify(self, method_name, *args, **kwargs):
        """JSON-RPC Notification. Notification means no response is expected.

        :param method_name: The remote procedure's method name.
        :param args: Positional arguments passed to the remote procedure.
        :param kwargs: Keyword arguments passed to the remote procedure.
        """
        return self.handle_response(
            self.send_message(rpc.request(method_name, *args, **kwargs)), False)

    def send_message(self, request):
        """Send the RPC request to the server. Override this method in the
        transport-specific subclass. Returns the response string.

        :param request: A JSON-RPC request, in dict format.
        """
        raise NotImplementedError(
            'The Server class is now abstract; '
            'use a transport-specific class such as HTTPServer instead')

    @staticmethod
    def handle_response(response, expected_response=False):
        """Processes the response and returns the 'result' portion if present.

        :param response: The JSON-RPC response string to process.
        :param expected_response: True if we were expecting a result
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
            # Validate the response against the Response schema
            try:
                jsonschema.validate(response_dict, json.loads(pkgutil.get_data(
                    __name__, 'response-schema.json').decode('utf-8')))
            except jsonschema.ValidationError:
                raise exceptions.InvalidResponse()
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
