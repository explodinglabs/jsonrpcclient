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
from tornado.httpclient import AsyncHTTPClient

from ..async_client import AsyncClient
from ..response import Response


class TornadoClient(AsyncClient):
    """
    Note: Tornado raises its own HTTP response status code exceptions, so there's no
    need to raise ReceivedNon2xxResponseError.

    :param endpoint: The server address.
    :param client: Tornado asynchronous HTTP client.
    :param kwargs: Keyword arguments to pass to the client initialiser.
    """

    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, *args, client=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client or AsyncHTTPClient()

    def log_response(self, response):
        # Note: Tornado adds it's own logger handlers, so the following log format isn't
        # used, unless Tornado's handlers are disabled.
        super().log_response(
            response,
            fmt="<-- %(message)s (%(http_code)s %(http_reason)s)",
            extra={
                "http_code": response.raw.code,
                "http_reason": response.raw.reason,
            },
        )

    async def send_message(self, request, **kwargs):
        """
        Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :param kwargs: Keyword arguments to the Tornado request.
        :return: The response (a string for requests, None for notifications).
        """
        headers = dict(self.DEFAULT_HEADERS)
        headers.update(kwargs.pop("headers", {}))

        response = await self.client.fetch(
            self.endpoint, method="POST", body=request, headers=headers, **kwargs
        )

        return Response(response.body.decode(), raw=response)
