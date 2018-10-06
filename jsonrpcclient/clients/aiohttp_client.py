"""
aiohttp client.

Requires aiohttp >= 3.0.
http://aiohttp.readthedocs.io/
"""
from ssl import SSLContext
from typing import Any, Optional

import async_timeout  # type: ignore
from aiohttp import ClientSession  # type: ignore

from ..async_client import AsyncClient
from ..exceptions import ReceivedNon2xxResponseError
from ..response import Response


class AiohttpClient(AsyncClient):

    DEFAULT_RESPONSE_LOG_FORMAT = "<-- %(message)s (%(http_code)s %(http_reason)s)"

    def __init__(
        self,
        session: ClientSession,
        endpoint: str,
        *args: Any,
        ssl: Optional[SSLContext] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.endpoint = endpoint
        self.session = session
        self.ssl = ssl

    def log_response(
        self, response: Response, trim_log_values: bool = False, **kwargs: Any
    ) -> None:
        extra = (
            {"http_code": response.raw.status, "http_reason": response.raw.reason}
            if response.raw is not None
            else {}
        )
        super().log_response(
            response, extra=extra, trim_log_values=trim_log_values, **kwargs
        )

    def validate_response(self, response: Response) -> None:
        if response.raw is not None and not 200 <= response.raw.status <= 299:
            raise ReceivedNon2xxResponseError(response.raw.status)

    async def send_message(
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
        with async_timeout.timeout(10):
            async with self.session.post(
                self.endpoint, data=request, ssl=self.ssl
            ) as response:
                response_text = await response.text()
                return Response(response_text, raw=response)
