"""An HTTP client to communicate with, for example::

    HTTPClient('http://example.com/api').request('go')

Uses the Requests library.
http://docs.python-requests.org/en/master/
"""

from requests import Request, Session

from .client import Client


class HTTPClient(Client):
    """Defines an HTTP client"""

    # The default HTTP header
    _DEFAULT_HEADERS = {
        'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __init__(self, endpoint):
        """
        :param endpoint: The server address.
        :param kwargs: HTTP headers and other options passed on to the requests
                       module.
        """
        super(HTTPClient, self).__init__(endpoint)
        # Make use of Requests' sessions feature
        self.session = Session()
        self.session.headers.update(self._DEFAULT_HEADERS)
        # Keep last request and response - don't use, will be removed in next
        # major release
        self.last_request = None
        self.last_response = None

    def _prepare_request(self, request, headers=None, files=None, params=None,
                         auth=None, cookies=None, **kwargs):
        """Prepare the request for sending.

        :param request: The JSON-RPC request (a PreparedRequest object)
        :param kwargs: Configuration for just this request
        :return: None
        """
        # Use the Requests library to prepare the request based on the session
        # configuration
        req = Request(method='POST', url=self.endpoint, data=request,
                      headers=headers, files=files, params=params, auth=auth,
                      cookies=cookies)
        request.prepped = self.session.prepare_request(req)
        # Include the http headers in log extra. Will not have effect unless
        # user configures the log format
        request.log_extra = {'http_headers': request.prepped.headers}

    def _send_message(self, request, stream=False, timeout=None, verify=True,
                      cert=None, proxies=None, **kwargs):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :param kwargs: Passed on to the requests lib's send function, for last
            minute configuration
        :return: The JSON-RPC response.
        :rtype: A string for requests, None for notifications.
        :raise requests.exceptions.RequestException:
            Raised by the requests module in the event of a communications
            error.
        """
        # Keep last request - don't use, will be removed in next major release
        self.last_request = request
        # Send the message with Requests, passing any final config options
        response = self.session.send(
            request.prepped, stream=stream, timeout=timeout, verify=verify,
            cert=cert, proxies=proxies)
        # Keep last response - don't use, will be removed in next major release
        self.last_response = response
        # Give some extra information to include in the response log entry
        return self._process_response(response.text, log_extra={
            'http_code': response.status_code, 'http_reason': response.reason,
            'http_headers': response.headers}, \
            log_format='<-- %(message)s (%(http_code)s %(http_reason)s)')
