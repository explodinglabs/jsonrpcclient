from .async_client import AsyncClient
import async_timeout

class aiohttpClient(AsyncClient):
    def __init__(self, session, url):
        self.session = session
        self.url = url

    async def _send_message(self, request):
        with async_timeout.timeout(10):
            async with self.session.post(self.url, data=request) as response:
                response = await response.text()
                return self._process_response(response)
