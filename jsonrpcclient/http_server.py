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
        """Instantiate a remote server object.
        >>> server = HTTPServer('http://example.com/api', \
                headers={'Content-Type': 'application/json-rpc'}, \
                auth=('user', 'pass'))
        """
        super(HTTPServer, self).__init__(endpoint)
        kwargs.setdefault('headers', self.DEFAULT_HTTP_HEADERS)
        self.headers = kwargs['headers']
        self.requests_kwargs = kwargs
        kwargs.pop('headers')

    def send_message(self, request):
        """Send the RPC request (a json dict) to the server.
        Raises JsonRpcClientError: On any error caught.
        Returns: Response string
        """
        s = Session()
        # Prepare the request
        request = Request(method='POST', url=self.endpoint, \
            headers=self.headers, json=request, **self.requests_kwargs)
        request = s.prepare_request(request)
        request.headers = dict(list(dict(request.headers).items()) + list(
            self.headers.items()))
        # Log the request before sending
        self.request_log.info(
            request.body,
            extra={
                'endpoint': self.endpoint,
                'http_headers': request.headers
            })
        try:
            response = s.send(request)
        # Catch the requests module's InvalidSchema exception if the outgoing
        # json is invalid.
        except InvalidSchema:
            raise exceptions.InvalidRequest()
        # Catch all other requests exceptions, such as network issues. See
        # http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        except RequestException: # Base requests exception
            raise exceptions.ConnectionError()
        finally:
            s.close()
        # Log the response, cleaning it up a bit
        self.response_log.info(
            response.text \
                .replace("\n", '').replace('  ', ' ').replace('{ ', '{'),
            extra={
                'endpoint': self.endpoint,
                'http_code': response.status_code,
                'http_reason': response.reason,
                'http_headers': response.headers
            })
        return response.text
