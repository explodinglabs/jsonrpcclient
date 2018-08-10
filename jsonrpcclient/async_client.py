"""
Asynchronous client.

Abstract base class for other asynchronous clients such as aiohttp, WebSockets & ZeroMQ.
"""
import json
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Union

from .client import Client
from .request import Request, Notification
from .response import Response
from .parse import parse


class AsyncClient(Client, metaclass=ABCMeta):
    @abstractmethod
    async def send_message(self, request: str, **kwargs) -> Response:  # type: ignore
        """Override to transport the request"""

    async def send(  # type: ignore
        self,
        request: Union[str, Dict, List],
        trim_log_values: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        if trim_log_values is None:
            trim_log_values = self.trim_log_values
        # Convert to string
        if isinstance(request, str):
            request_text = request
        else:
            request_text = json.dumps(request)
        self.log_request(request_text, trim=trim_log_values)
        response = await self.send_message(request_text, **kwargs)
        self.log_response(response, trim=trim_log_values)
        self.validate_response(response)
        response.data = parse(response.text, validate_against_schema=self.validate_against_schema)
        return response

    async def notify(  # type: ignore
        self,
        method_name: str,
        *args: Any,
        trim_log_values: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        if trim_log_values is None:
            trim_log_values = self.trim_log_values
        return await self.send(
            Notification(method_name, *args, **kwargs), trim_log_values=trim_log_values
        )

    async def request(  # type: ignore
        self,
        method_name: str,
        *args: Any,
        trim_log_values: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        if trim_log_values is None:
            trim_log_values = self.trim_log_values
        return await self.send(
            Request(method_name, *args, **kwargs), trim_log_values=trim_log_values
        )
