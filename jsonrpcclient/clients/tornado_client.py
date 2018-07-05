"""
Tornado Client
**************

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

from ..async_client import AsyncClient
from ..exceptions import ReceivedNon2xxResponseError


class TornadoClient(AsyncClient):
    """
    :param endpoint: The server address.
    :param async_http_client_class: Tornado asynchronous HTTP client class.
    :param kwargs: Keyword arguments to pass to the client initialiser.
    """

    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, *args, async_http_client=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_client = async_http_client or AsyncHTTPClient()

    async def send_message(self, request, **kwargs):
        """
        Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :param kwargs: Keyword arguments to the Tornado request.
        :return: The response (a string for requests, None for notifications).
        """
        headers = dict(self.DEFAULT_HEADERS)
        headers.update(kwargs.pop("headers", {}))

        response = await self.http_client.fetch(
            self.endpoint, method="POST", body=request, headers=headers, **kwargs
        )

        if not 200 <= response.code <= 299:
            raise ReceivedNon2xxResponseError(response.status_code)

        # Note: Tornado adds it's own logger handlers, so the following log format isn't
        # used, unless Tornado's handlers are disabled.
        return self.process_response(
            response.body.decode(),
            log_extra={"http_code": response.code, "http_reason": response.reason},
            log_format="<-- %(message)s (%(http_code)s %(http_reason)s)",
        )
