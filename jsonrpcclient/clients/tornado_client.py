"""
Tornado Client.

Represents an endpoint to communicate with using Tornado asynchronous HTTP client.
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
    DEFAULT_RESPONSE_LOG_FORMAT = "<-- %(message)s (%(http_code)s %(http_reason)s)"

    def __init__(
        self,
        endpoint: str,
        *args: Any,
        client: Optional[AsyncHTTPClient] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.endpoint = endpoint
        self.client = client or AsyncHTTPClient()

    def log_response(
        self, response: Response, trim_log_values: bool = False, **kwargs: Any
    ) -> None:
        extra = (
            {"http_code": response.raw.code, "http_reason": response.raw.reason}
            if response.raw is not None
            else {}
        )
        super().log_response(
            response, extra=extra, trim_log_values=trim_log_values, **kwargs
        )

    async def send_message(  # type: ignore
        self, request: str, response_expected: bool, **kwargs: Any
    ) -> Response:
        """
        Transport the message to the server and return the response.

        Args:
            request: The JSON-RPC request string.
            response_expected: Whether the request expects a response.

        Returns:
            A Response object.
        """
        headers = dict(self.DEFAULT_HEADERS)
        headers.update(kwargs.pop("headers", {}))

        response = await self.client.fetch(
            self.endpoint, method="POST", body=request, headers=headers, **kwargs
        )

        return Response(response.body.decode(), raw=response)
