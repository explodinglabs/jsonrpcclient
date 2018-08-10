"""
Websockets client.

http://websockets.readthedocs.io/
"""
from ..async_client import AsyncClient
from ..response import Response


class WebSocketsClient(AsyncClient):
    def __init__(self, socket, *args, **kwargs):
        """
        :param endpoint:
        :param socket_type:
        :param *args: Passed through to Client class.
        :param **kwargs: Passed through to Client class.
        """
        super().__init__(*args, **kwargs)
        self.socket = socket

    async def send_message(self, request, **kwargs):
        await self.socket.send(request)
        response_text = await self.socket.recv()
        return Response(response_text)
