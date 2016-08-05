"""
HTTPServer
**********

An HTTP server to communicate with, for example::

    HTTPServer('http://example.com/api').request('go')
"""

from requests import Request, Session

from jsonrpcclient.server import Server


class HTTPServer(Server):
    """
    :param endpoint: The server address.
    :param kwargs: HTTP headers and other options passed on to the requests
                   module.
    """

    # The default HTTP header
    __DEFAULT_HTTP_HEADERS__ = {
        'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __init__(self, endpoint):
        super(HTTPServer, self).__init__(endpoint)
        self.session = Session()
        self.session.headers.update(self.__DEFAULT_HTTP_HEADERS__)
        self.last_request = None
        self.last_response = None

    def _send_message(
            self, request, headers=None, files=None, params=None, auth=None,
            cookies=None, **kwargs):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The JSON-RPC response.
        :rtype: A string for requests, None for notifications.
        :raise requests.exceptions.RequestException:
            Raised by the requests module in the event of a communications
            error.
        """
        # Prepare the request
        req = Request(
            method='POST', url=self.endpoint, data=request, headers=headers,
            files=files, params=params, auth=auth, cookies=cookies)
        prepped = self.session.prepare_request(req)
        self.last_request = prepped
        # Log the request
        self._log_request(request, {'http_headers': prepped.headers})
        # Send the message
        response = self.session.send(prepped, **kwargs)
        # Log the response
        self._log_response(response.text, {'http_code': response.status_code, \
            'http_reason': response.reason, 'http_headers': response.headers})
        self.last_response = response
        return response.text
