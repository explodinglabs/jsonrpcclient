"""
Tornado Client
**************

Represents an endpoint to communicate with using Tornado asynchronous HTTP
client.
"""
from tornado.httpclient import AsyncHTTPClient

from ..async_client import AsyncClient
from ..response import Response


class TornadoClient(AsyncClient):
    """
    Note: Tornado raises its own HTTP response status code exceptions, so there's no
    need to raise ReceivedNon2xxResponseError.
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
        headers = dict(self.DEFAULT_HEADERS)
        headers.update(kwargs.pop("headers", {}))

        response = await self.client.fetch(
            self.endpoint, method="POST", body=request, headers=headers, **kwargs
        )

        return Response(response.body.decode(), raw=response)
