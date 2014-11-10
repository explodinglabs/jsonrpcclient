"""server.py"""

import json
import logging
import pkgutil

import requests
import jsonschema

from . import rpc
from . import exceptions

class Server:
    """This class acts as the remote server"""

    def __init__(self, endpoint):
        self.endpoint = endpoint

        self.logger = logging.getLogger('jsonrpcclient')
        self.logger.addHandler(logging.StreamHandler())

    def __getattr__(self, name):
        """Catch undefined methods and handle them as RPC requests.

        The technique is here:
        http://code.activestate.com/recipes/307618/
        """

        def attr_handler(*args, **kwargs):
            """Call self.request from here"""
            return self.request(name, *args, **kwargs)

        return attr_handler

    def request(self, method_name, *args, **kwargs):
        """Send the request and expect a response."""

        kwargs['response'] = True
        return self.handle_response(
            self.send_message(rpc.request(method_name, *args, **kwargs)), True)

    def notify(self, method_name, *args, **kwargs):
        """Really just an alias for _send()"""

        return self.handle_response(
            self.send_message(rpc.request(method_name, *args, **kwargs)), False)

    def send_message(self, request_dict):
        """Send the RPC request to the server.

        Calls a procedure on another server.
        Raises RPCClientException: On any error caught.
        """

        # Log the request
        self.logger.debug('--> '+json.dumps(request_dict))

        try:
            # Send the message
            r = requests.post(
                self.endpoint,
                headers={
                    'Content-Type': 'application/json; charset=utf-8'
                },
                json=request_dict
            )

        except (requests.exceptions.InvalidSchema,
                requests.exceptions.RequestException):
            raise exceptions.ConnectionError()

        if len(r.text):
            # Log the response
            self.logger.debug('<-- '+r.text \
                .replace("\n",'') \
                .replace('  ', ' ')
                .replace('{ ', '{')
                )

        else:
            self.logger.debug('<-- {} {}'.format(r.status_code, r.reason))

            # Raise exception the HTTP status code was not 200, and there was no
            # response body, because this should be handled.
            if r.status_code != 200:
                raise exceptions.StatusCodeError(r.status_code)

        return r.text

    @staticmethod
    def handle_response(response_str, expected_response=True):
        """Processes the response from a request"""

        # A response was expected, but none was given?
        if expected_response and not len(response_str):
            raise exceptions.ReceivedNoResponse()

        # Was response given?
        if len(response_str):

            # Attempt to parse the response
            try:
                response_dict = json.loads(response_str)

            except ValueError:
                raise exceptions.ParseError()

            # A response was *not* expected, but one was given? It may not
            # be necessary to raise here. If we receive a response anyway,
            # can't we just ignore it?
            if not expected_response and 'result' in response_dict:
                raise exceptions.InvalidResponse()

            # Validate the response against the Response schema
            try:
                jsonschema.validate(
                    response_dict,
                    json.loads(pkgutil.get_data(
                        __name__, 'response-schema.json').decode('utf-8')))

            except jsonschema.ValidationError:
                raise exceptions.InvalidResponse()

            # If the response was "error", raise it, to ensure it's handled
            if 'error' in response_dict:
                raise exceptions.ReceivedErrorResponse(
                    response_dict['error']['code'],
                    response_dict['error']['message'])

            # Otherwise, surely we have a result to return
            print(response_dict['result'])

        return None
