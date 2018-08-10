"""
Asynchronous client.

Abstract base class for other asynchronous clients such as aiohttp, WebSockets & ZeroMQ.
"""
import json
from abc import ABCMeta, abstractmethod
from typing import Union, Dict, List

from .client import Client
from .request import Request, Notification
from .response import Response


class AsyncClient(Client, metaclass=ABCMeta):
    @abstractmethod
    async def send_message(self, request: str, **kwargs) -> Response:  # type: ignore
        """Override to transport the request"""

    async def send(self, request: Union[str, Dict, List], **kwargs) -> Response:  # type: ignore
        # Convert to string
        if isinstance(request, str):
            request_text = request
        else:
            request_text = json.dumps(request)
        self.log_request(request_text)
        response = await self.send_message(request_text, **kwargs)
        self.log_response(response)
        self.validate_response(response)
        response.parse(validate_against_schema=self.validate_against_schema)
        return response

    async def notify(self, method_name: str, *args, **kwargs):  # type: ignore
        return await self.send(Notification(method_name, *args, **kwargs))

    async def request(self, method_name: str, *args, **kwargs):  # type: ignore
        return await self.send(Request(method_name, *args, **kwargs))
