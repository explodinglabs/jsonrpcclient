import zmq
import zmq.asyncio
from .async_client import AsyncClient

class ZeroMQAsyncClient(AsyncClient):
    def __init__(self, endpoint, socket_type=zmq.REQ):
        super(ZeroMQAsyncClient, self).__init__(endpoint)
        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    async def _send_message(self, request, **kwargs):
        await self.socket.send_multipart((request.encode(),))
        response = await self.socket.recv_multipart()
        return self._process_response(response[0].decode())
