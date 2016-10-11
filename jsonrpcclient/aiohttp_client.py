"""aiohttp http://aiohttp.readthedocs.io/"""

import async_timeout
from .async_client import AsyncClient

class aiohttpClient(AsyncClient):
    """TODO: rename aiohttpClient to AiohttpClient (breaking change)"""
    def __init__(self, session, endpoint):
        super(aiohttpClient, self).__init__(endpoint)
        self.session = session

    async def _send_message(self, request):
        with async_timeout.timeout(10):
            async with self.session.post(self.endpoint, data=request) \
                    as response:
                response = await response.text()
                return self._process_response(response)
