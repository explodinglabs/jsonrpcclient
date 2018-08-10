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

    def __init__(self, session: ClientSession, endpoint: str) -> None:
        super().__init__(endpoint)
        self.session = session

    def log_response(
        self, response: Response, fmt: str = None, trim: bool = False, **kwargs: Any
    ) -> None:
        super().log_response(
            response,
            extra={
                "http_code": response.raw.status,  # type: ignore
                "http_reason": response.raw.reason,  # type: ignore
            },
            fmt="<-- %(message)s (%(http_code)s %(http_reason)s)",
            trim=trim,
            **kwargs,
        )

    def validate_response(self, response: Response) -> None:
        if not 200 <= response.raw.status <= 299:  # type: ignore
            raise ReceivedNon2xxResponseError(response.raw.status)  # type: ignore

    async def send_message(self, request: str) -> Response:  # type: ignore
        with async_timeout.timeout(10):
            async with self.session.post(self.endpoint, data=request) as response:
                response_text = await response.text()
                return Response(response_text, raw=response)
