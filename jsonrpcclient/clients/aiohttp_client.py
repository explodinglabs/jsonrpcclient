"""
aiohttp client.

http://aiohttp.readthedocs.io/
"""
import async_timeout

from ..async_client import AsyncClient
from ..exceptions import ReceivedNon2xxResponseError


class AiohttpClient(AsyncClient):
    """TODO: rename AiohttpClient to AiohttpClient"""

    def __init__(self, session, endpoint):
        super().__init__(endpoint)
        self.session = session

    async def send_message(self, request):
        with async_timeout.timeout(10):
            async with self.session.post(self.endpoint, data=request) as response:
                if not 200 <= response.status <= 299:
                    raise ReceivedNon2xxResponseError(response.status)
                return self.process_response(
                    await response.text(),
                    log_extra={
                        "http_code": response.status,
                        "http_reason": response.reason,
                    },
                    log_format="<-- %(message)s (%(http_code)s %(http_reason)s)",
                )
