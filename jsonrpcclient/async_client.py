"""Abstract base class for asynchronous clients"""
from abc import ABCMeta, abstractmethod

from future.utils import with_metaclass

from .client import Client
from .request import Request, Notification
from .prepared_request import PreparedRequest

class AsyncClient(with_metaclass(ABCMeta, Client)):
    @abstractmethod
    async def _send_message(self, request, **kwargs):
        """Abstract"""

    async def send(self, request, **kwargs):
        request = PreparedRequest(request)
        self._prepare_request(request, **kwargs)
        self._log_request(request, request.log_extra, request.log_format)
        return await self._send_message(request, **kwargs)

    async def notify(self, method_name, *args, **kwargs):
        return await self.send(Notification(method_name, *args, **kwargs))

    async def request(self, method_name, *args, **kwargs):
        return await self.send(Request(method_name, *args, **kwargs))
