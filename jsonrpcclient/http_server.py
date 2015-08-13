"""http_server.py"""

from requests import Request, Session
from requests.exceptions import InvalidSchema, RequestException

from . import exceptions
from .server import Server


class HTTPServer(Server):
    """HTTP transport"""

    # The default HTTP header, used if no others are specified
    DEFAULT_HTTP_HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, endpoint, **kwargs):
        """A remote HTTP server.

        Example usage::

            server = HTTPServer('http://example.com/api', \
                headers={'Content-Type': 'application/json-rpc'}, \
                auth=('user', 'pass'))

        :param endpoint: The remote server address.
        :param kwargs: Can be used to customize the HTTP headers used, and
            specify other options for the requests-module.
        """
        super(HTTPServer, self).__init__(endpoint)
        kwargs.setdefault('headers', self.DEFAULT_HTTP_HEADERS)
        self.headers = kwargs['headers']
        self.requests_kwargs = kwargs
        kwargs.pop('headers')

    def send_message(self, request):
        """Transport the request to the server and return the response.

        :param request: The JSON-RPC request, in dict format.
        """
        # Prepare the request
        session = Session()
        request = Request(method='POST', url=self.endpoint, \
            headers=self.headers, json=request, **self.requests_kwargs)
        request = session.prepare_request(request)
        request.headers = dict(list(dict(request.headers).items()) + list(
            self.headers.items()))
        # Log the request
        self.log_request(request.body, {'http_headers': request.headers})
        try:
            response = session.send(request)
        # If the outgoing JSON request is invalid, the requests module raises
        # InvalidSchema
        except InvalidSchema:
            raise exceptions.InvalidRequest()
        # Catch all other Requests exceptions, such as network issues
        except RequestException: # Base Requests exception
            raise exceptions.ConnectionError()
        finally:
            session.close()
        # Log the response
        self.log_response(response.text, {'http_code': response.status_code, \
            'http_reason': response.reason, 'http_headers': response.headers})
        return response.text
