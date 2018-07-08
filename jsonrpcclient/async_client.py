"""
Asynchronous client.

Abstract base class for other asynchronous clients such as WebSockets, ZeroMQ
and aiohttp.
"""
from abc import ABCMeta, abstractmethod

from .client import Client
from .request import Request, Notification
from .prepared_request import PreparedRequest


class AsyncClient(Client, metaclass=ABCMeta):
    @abstractmethod
    async def send_message(self, request, **kwargs):
        """(Abstract)"""

    async def send(self, request, **kwargs):
        request = PreparedRequest(request)
        self.prepare_request(request, **kwargs)
        self.log_request(request, request.log_extra, request.log_format)
        return await self.send_message(request, **kwargs)

    async def notify(self, method_name, *args, **kwargs):
        return await self.send(Notification(method_name, *args, **kwargs))

    async def request(self, method_name, *args, **kwargs):
        return await self.send(Request(method_name, *args, **kwargs))
