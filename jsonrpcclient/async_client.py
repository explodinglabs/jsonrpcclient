"""
Asynchronous client.

Abstract base class for other asynchronous clients such as aiohttp, WebSockets & ZeroMQ.
"""
from abc import ABCMeta, abstractmethod

from .client import Client
from .request import Request, Notification
from .response import Response


class AsyncClient(Client, metaclass=ABCMeta):
    @abstractmethod
    async def send_message(self, request, **kwargs):
        """Override to transport the request"""

    async def send(self, request, **kwargs):
        # Convert to string
        if isinstance(request, Notification):  # Includes Requests
            request = str(request)
        elif not isinstance(request, str):
            request = json.dumps(request)
        self.log_request(request)
        response = await self.send_message(request, **kwargs)
        self.log_response(response)
        self.validate_response(response)
        response.parse(validate_against_schema=self.validate_against_schema)
        return response

    async def notify(self, method_name, *args, **kwargs):
        return await self.send(Notification(method_name, *args, **kwargs))

    async def request(self, method_name, *args, **kwargs):
        return await self.send(Request(method_name, *args, **kwargs))
