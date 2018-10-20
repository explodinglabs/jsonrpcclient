"""Parse response text, returning JSONRPCResponse objects."""
from json import loads as deserialize
from typing import Any, Dict, List, Union

import jsonschema  # type: ignore
from pkg_resources import resource_string

from .response import (
    ErrorResponse,
    JSONRPCResponse,
    NotificationResponse,
    SuccessResponse,
)

schema = deserialize(resource_string(__name__, "response-schema.json").decode())


def get_response(response: Dict[str, Any]) -> JSONRPCResponse:
    """
    Converts a deserialized response into a JSONRPCResponse object.

    The dictionary be either an error or success response, never a notification.

    Args:
        response: Deserialized response dictionary. We can assume the response is valid
            JSON-RPC here, since it passed the jsonschema validation.
    """
    if "error" in response:
        return ErrorResponse(**response)
    return SuccessResponse(**response)


def parse(
    response_text: str, *, batch: bool, validate_against_schema: bool = True
) -> Union[JSONRPCResponse, List[JSONRPCResponse]]:
    """
    Parses response text, returning JSONRPCResponse objects.

    Args:
        response_text: JSON-RPC response string.
        batch: If the response_text is an empty string, this determines how to parse.
        validate_against_schema: Validate against the json-rpc schema.

    Returns:
        Either a JSONRPCResponse, or a list of them.

    Raises:
        json.JSONDecodeError: The response was not valid JSON.
        jsonschema.ValidationError: The response was not a valid JSON-RPC response
            object.
    """
    # If the response is empty, we can't deserialize it; an empty string is valid
    # JSON-RPC, but not valid JSON.
    if not response_text:
        if batch:
            # An empty string is a valid response to a batch request, when there were
            # only notifications in the batch.
            return []
        else:
            # An empty string is valid response to a Notification request.
            return NotificationResponse()

    # If a string, ensure it's json-deserializable
    deserialized = deserialize(response_text)

    # Validate the response against the Response schema (raises
    # jsonschema.ValidationError if invalid)
    if validate_against_schema:
        jsonschema.validate(deserialized, schema)

    # Batch response
    if isinstance(deserialized, list):
        return [get_response(r) for r in deserialized if "id" in r]
    # Single response
    return get_response(deserialized)
