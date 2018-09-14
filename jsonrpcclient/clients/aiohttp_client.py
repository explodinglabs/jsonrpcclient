"""
aiohttp client.

http://aiohttp.readthedocs.io/
"""
from typing import Any

import async_timeout  # type: ignore
from aiohttp import ClientSession  # type: ignore

from ..async_client import AsyncClient
from ..exceptions import ReceivedNon2xxResponseError
from ..response import Response


class AiohttpClient(AsyncClient):
    """TODO: rename AiohttpClient to AiohttpClient"""

    DEFAULT_RESPONSE_LOG_FORMAT = "<-- %(message)s (%(http_code)s %(http_reason)s)"

    def __init__(
        self, session: ClientSession, endpoint: str, *args: Any, ssl=None, **kwargs: Any
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

    async def send_message(self, request: str) -> Response:  # type: ignore
        with async_timeout.timeout(10):
            async with self.session.post(self.endpoint, data=request, ssl=self.ssl) as response:
                response_text = await response.text()
                return Response(response_text, raw=response)
