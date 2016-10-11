"""Websockets http://websockets.readthedocs.io/"""
from .async_client import AsyncClient

class WebSocketsClient(AsyncClient):
    def __init__(self, socket):
        super(WebSocketsClient, self).__init__(None)
        self.socket = socket

    async def _send_message(self, request, **kwargs):
        await self.socket.send(request)
        response = await self.socket.recv()
        return self._process_response(response)
