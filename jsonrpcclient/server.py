"""server.py"""

import json
import pkgutil

from requests import Request, Session
from requests.exceptions import InvalidSchema, RequestException
import jsonschema

from jsonrpcclient import rpc
from jsonrpcclient import exceptions
from jsonrpcclient import request_log, response_log


DEFAULT_HTTP_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

class Server(object):
    """This class acts as the remote server"""

    def __init__(self, endpoint, **kwargs):
        """Instantiate a remote server object.

        >>> server = Server('http://example.com/api', \
                headers={'Content-Type': 'application/json-rpc'}, \
                auth=('user', 'pass'))
        """

        kwargs.setdefault('headers', DEFAULT_HTTP_HEADERS)

        self.endpoint = endpoint
        self.headers = kwargs['headers']
        self.requests_kwargs = kwargs

        kwargs.pop('headers')

    def __getattr__(self, name):
        """Catch undefined methods and handle them as RPC requests.

        The technique is here:
        http://code.activestate.com/recipes/307618/
        """

        def attr_handler(*args, **kwargs):
            """Call self.request from here"""

            if kwargs.get('response', False):
                return self.request(name, *args, **kwargs)
            else:
                return self.notify(name, *args, **kwargs)

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

    def send_message(self, request):
        """Send the RPC request to the server.

        Calls a procedure on another server.
        Raises JsonRpcClientError: On any error caught.
        """

        s = Session()

        # Prepare the request
        request = Request(method='POST', url=self.endpoint, \
            headers=self.headers, json=request, **self.requests_kwargs)
        request = s.prepare_request(request)

        request.headers = dict(list(dict(request.headers).items()) + list(
            self.headers.items()))

        # Log the request before sending
        request_log.info(
            request.body,
            extra={
                'http_headers': request.headers
            })

        try:
            response = s.send(request)
        # Catch the requests module's InvalidSchema exception if the json is
        # invalid.
        except InvalidSchema:
            raise exceptions.InvalidRequest()
        # Catch all other requests exceptions, such as network issues.
        # See http://stackoverflow.com/questions/16511337/
        except RequestException: # Base requests exception
            raise exceptions.ConnectionError()
        finally:
            s.close()

        # Log the response, cleaning it up a bit
        response_log.info(
            response.text \
                .replace("\n", '').replace('  ', ' ').replace('{ ', '{'),
            extra={
                'http_code': response.status_code,
                'http_reason': response.reason,
                'http_headers': response.headers
            })

        return response

    @staticmethod
    def handle_response(response, expected_response=False):
        """Processes the response from a request"""

        # A response was expected, but none was given?
        if expected_response and not len(response.text):
            raise exceptions.ReceivedNoResponse()

        # Was response given?
        if len(response.text):

            # Attempt to parse the response
            try:
                response_dict = json.loads(response.text)
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

            # If the response was "error", raise it, to ensure it's handled
            if 'error' in response_dict:
                raise exceptions.ReceivedErrorResponse(
                    response_dict['error']['code'],
                    response_dict['error']['message'])

            # Raise exception the HTTP status code was not 200.
            if response.status_code != 200:
                raise exceptions.Non200Response(response.status_code)

             # Otherwise, surely we have a result to return
            return response_dict['result']

        # Raise exception the HTTP status code was not 200.
        if response.status_code != 200:
            raise exceptions.Non200Response(response.status_code)

        return None
