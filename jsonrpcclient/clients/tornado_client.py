"""
Tornado Client.

Represents an endpoint to communicate with using Tornado asynchronous HTTP
client.
"""
from typing import Any, Optional

from tornado.httpclient import AsyncHTTPClient  # type: ignore

from ..async_client import AsyncClient
from ..response import Response


class TornadoClient(AsyncClient):
    """
    Note: Tornado raises its own HTTP response status code exceptions, so there's no
    need to raise ReceivedNon2xxResponseError.
    """

    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(
        self, *args: Any, client: Optional[AsyncHTTPClient] = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.client = client or AsyncHTTPClient()

    def log_response(
        self, response: Response, fmt: str = None, trim_log_values: bool = False, **kwargs: Any
    ) -> None:
        # Note: Tornado adds it's own log handlers, so the following log format isn't
        # used unless Tornado's handlers are disabled.
        super().log_response(
            response,
            extra={
                "http_code": response.raw.code,  # type: ignore
                "http_reason": response.raw.reason,  # type: ignore
            },
            fmt="<-- %(message)s (%(http_code)s %(http_reason)s)",
            trim_log_values=trim_log_values,
            **kwargs,
        )

    async def send_message(  # type: ignore
        self, request: str, **kwargs: Any
    ) -> Response:
        headers = dict(self.DEFAULT_HEADERS)
        headers.update(kwargs.pop("headers", {}))

        response = await self.client.fetch(
            self.endpoint, method="POST", body=request, headers=headers, **kwargs
        )

        return Response(response.body.decode(), raw=response)
