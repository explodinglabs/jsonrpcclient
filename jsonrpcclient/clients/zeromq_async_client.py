"""ZeroMQ Client"""
import zmq
import zmq.asyncio

from ..async_client import AsyncClient


class ZeroMQAsyncClient(AsyncClient):
    """
    :param endpoint:
    :param socket_type:
    :param *args: Passed through to Client class.
    :param **kwargs: Passed through to Client class.
    """
    def __init__(self, endpoint, *args, socket_type=zmq.REQ, **kwargs):
        super().__init__(endpoint, *args, **kwargs)
        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    async def send_message(self, request, **kwargs):
        await self.socket.send_multipart((request.encode(),))
        response = await self.socket.recv_multipart()
        return self.process_response(response[0].decode())
