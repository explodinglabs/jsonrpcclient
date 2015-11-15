"""
HTTPServer
**********

An HTTP server to communicate with, for example::

    HTTPServer('http://example.com/api').request('go')
"""

from requests import Request, Session
from requests.exceptions import RequestException

from jsonrpcclient.server import Server


class HTTPServer(Server):
    """
    :param endpoint: The server address.
    :param kwargs: HTTP headers and other options passed on to the requests
                   module.
    """

    # The default HTTP header, these are used if no other headers are specified
    DEFAULT_HTTP_HEADERS = {
        'Content-Type': 'application/json', 'Accept':
        'application/json'}

    def __init__(self, endpoint, **kwargs):
        super(HTTPServer, self).__init__(endpoint)
        kwargs.setdefault('headers', self.DEFAULT_HTTP_HEADERS)
        self.headers = kwargs['headers']
        self.requests_kwargs = kwargs
        kwargs.pop('headers')

    def send_message(self, request):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response (a string for requests, None for notifications).
        """
        # Prepare the session
        session = Session()
        session_request = Request(method='POST', url=self.endpoint, \
            headers=self.headers, data=request, **self.requests_kwargs)
        prepared_request = session.prepare_request(session_request)
        prepared_request.headers = dict(list(dict(
            prepared_request.headers).items()) + list(self.headers.items()))
        # Log the request
        self.log_request(request, {'http_headers': prepared_request.headers})
        # Send the message
        try:
            response = session.send(prepared_request)
        except RequestException:
            session.close()
            raise
        session.close()
        # Log the response
        self.log_response(response.text, {'http_code': response.status_code, \
            'http_reason': response.reason, 'http_headers': response.headers})
        return response.text
