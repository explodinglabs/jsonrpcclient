"""
Async client.
"""
from abc import ABCMeta, abstractmethod
from json import dumps as serialize
from json import loads as deserialize
from typing import Any, Dict, Iterator, List, Optional, Union

from apply_defaults import apply_self  # type: ignore

from .client import Client
from .exceptions import ReceivedErrorResponseError
from .parse import parse
from .requests import Notification, Request
from .response import ErrorResponse, Response


class AsyncClient(Client, metaclass=ABCMeta):
    """
    Abstract base class for the asynchronous clients.

    Has async versions of the Client class's public methods.
    """

    @abstractmethod
    async def send_message(
        self, request: str, response_expected: bool, **kwargs: Any
    ) -> Response:
        """Override to transport the request"""

    @apply_self
    async def send(
        self,
        request: Union[str, Dict, List],
        trim_log_values: bool = False,
        validate_against_schema: bool = True,
        **kwargs: Any
    ) -> Response:
        """
        Async version of Client.send.
        """
        # We need both the serialized and deserialized version of the request
        if isinstance(request, str):
            request_text = request
            request_deserialized = deserialize(request)
        else:
            request_text = serialize(request)
            request_deserialized = request
        batch = isinstance(request_deserialized, list)
        response_expected = batch or "id" in request_deserialized
        self.log_request(request_text, trim_log_values=trim_log_values)
        response = await self.send_message(
            request_text, response_expected=response_expected, **kwargs
        )
        self.log_response(response, trim_log_values=trim_log_values)
        self.validate_response(response)
        response.data = parse(
            response.text, batch=batch, validate_against_schema=validate_against_schema
        )
        # If received a single error response, raise
        if isinstance(response.data, ErrorResponse):
            raise ReceivedErrorResponseError(response.data)
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
        """
        Async version of Client.notify.
        """
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
        """
        Async version of Client.request.
        """
        return await self.send(
            Request(method_name, id_generator=id_generator, *args, **kwargs),
            trim_log_values=trim_log_values,
            validate_against_schema=validate_against_schema,
        )
