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

    # The default HTTP header
    DEFAULT_HTTP_HEADERS = {
        'Content-Type': 'application/json', 'Accept':
        'application/json'}

    def __init__(self, endpoint, **kwargs):
        super(HTTPServer, self).__init__(endpoint)
        # Set the default headers if none were passed
        self.session = Session()
        self.request_args = {'headers': self.DEFAULT_HTTP_HEADERS}
        print(self.request_args)
        self.request_args.update(kwargs)
        print(self.request_args)

    def send_message(self, request, **kwargs):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response.
        :rtype: A string for requests, None for notifications.
        :raise requests.exceptions.RequestException:
            Raised by the requests module in the event of a communications error.
        """
        # Settings to pass to Request(). Merge with global ones.
        request_args = self.request_args.copy()
        request_args.update(**kwargs)
        # Prepare the request - we're using prepared requests because it gives
        # more information for logging
        request = Request(method='POST', url=self.endpoint, data=request, \
                **request_args)
        prepped = self.session.prepare_request(request)
        self.last_request = prepped
        # Log the request
        self.log_request(request, {'http_headers': prepped.headers})
        # Send the message
        response = self.session.send(prepped)
        # Log the response
        self.log_response(response.text, {'http_code': response.status_code, \
            'http_reason': response.reason, 'http_headers': response.headers})
        self.last_response = response
        return response.text
