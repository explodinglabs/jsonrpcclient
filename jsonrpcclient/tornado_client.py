"""
TornadoClient
*************

Represents an endpoint to communicate with using Tornado asynchronous HTTP
client::

    from tornado import ioloop

    async def test():
        client = TornadoClient('http://example.com/api')
        result = await yield client.some_method(42)
        print(result)

    ioloop.IOLoop.instance().run_sync(test)
"""
from functools import partial

from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future

from .client import Client


class TornadoClient(Client):
    """
    :param endpoint: The server address.
    :param async_http_client_class: Tornado asynchronous HTTP client class.
    :param kwargs: Keyword arguments to pass to the client initialiser.
    """

    _DEFAULT_HEADERS = {
        'Content-Type' : 'application/json',
        'Accept'       : 'application/json'
    }


    def __init__(self, endpoint, async_http_client_class=AsyncHTTPClient, \
            **kwargs):
        super(TornadoClient, self).__init__(endpoint)
        self.http_client = async_http_client_class(**kwargs)

    def _request_sent(self, future, response):
        """Callback when request has been sent"""
        if response.error:
            future.set_exception(response.error)
        else:
            future.set_result(self._process_response(response.body.decode(), {
                'http_code': response.code, 'http_reason': response.reason,
                'http_headers' : response.headers}))

    def _send_message(self, request, **kwargs):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :param kwargs: Keyword arguments to the Tornado request.
        :return: The response (a string for requests, None for notifications).
        """
        headers = dict(self._DEFAULT_HEADERS)
        headers.update(kwargs.get('headers', {}))

        future = Future()
        self.http_client.fetch(
            self.endpoint, method='POST', body=request, headers=headers,
            callback=partial(self._request_sent, future), **kwargs)
        return future
