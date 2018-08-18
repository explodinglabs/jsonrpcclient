"""
Async client.

Abstract base class for the asynchronous clients.

Has async versions of the Client class's public methods.
"""
import json
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterator, List, Optional, Union

from apply_defaults import apply_self  # type: ignore

from .client import Client
from .parse import parse
from .request import Notification, Request
from .response import Response


class AsyncClient(Client, metaclass=ABCMeta):
    @abstractmethod
    async def send_message(self, request: str, **kwargs) -> Response:  # type: ignore
        """Override to transport the request"""

    @apply_self
    async def send(
        self,
        request: Union[str, Dict, List],
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
        **kwargs: Any
    ) -> Response:
        # Convert the request to a string if it's not already.
        request_text = request if isinstance(request, str) else json.dumps(request)
        self.log_request(request_text, trim_log_values=trim_log_values)
        response = await self.send_message(request_text, **kwargs)
        self.log_response(response, trim_log_values=trim_log_values)
        self.validate_response(response)
        response.data = parse(
            response.text, validate_against_schema=validate_against_schema
        )
        return response

    @apply_self
    async def notify(
        self,
        method_name: str,
        *args: Any,
        trim_log_values: Optional[bool] = None,
        validate_against_schema: Optional[bool] = None,
        **kwargs: Any
    ) -> Response:
        return await self.send(
            Notification(method_name, *args, **kwargs),
            trim_log_values=trim_log_values,
            validate_against_schema=validate_against_schema,
        )

    @apply_self
    async def request(
        self,
        method_name: str,
        *args: Any,
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
        id_generator: Optional[Iterator] = None,
        **kwargs: Any
    ) -> Response:
        return await self.send(
            Request(method_name, id_generator=id_generator, *args, **kwargs),
            trim_log_values=trim_log_values,
            validate_against_schema=validate_against_schema,
        )
