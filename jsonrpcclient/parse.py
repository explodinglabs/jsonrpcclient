"""
Parse response text, returning JSONRPCResponse objects.
"""
from typing import List, Union
from json import loads as deserialize, JSONDecodeError

import jsonschema  # type: ignore
from pkg_resources import resource_string

from . import exceptions
from .response import JSONRPCResponse

schema = deserialize(resource_string(__name__, "response-schema.json").decode())


def parse(
    response_text: str, *, batch: bool, validate_against_schema: bool = True
) -> Union[JSONRPCResponse, List[JSONRPCResponse]]:
    """
    Parses response text, returning JSONRPCResponse objects.

    Args:
        response_text: JSON-RPC response string.
        is_batch_request: If the response_text is an empty string, this determines how
            to parse.
        validate_against_schema: Validate against the json-rpc schema.

    Returns:
        Either a JSONRPCResponse, or a list of them.

    Raises:
        json.JSONDecodeError: The response was not valid JSON.
        jsonschema.ValidationError: The response was not a valid JSON-RPC response
            object.
    """
    # If the response is empty, we can't deserialize it. The return value depends on if
    # it's responding to a batch request or not.
    if not response_text:
        if batch:
            # An empty string is a valid response to a batch request, when there were
            # only notifications in the batch.
            return []
        else:
            # An empty string is valid response to a Notification request.
            return JSONRPCResponse(None)

    # If a string, ensure it's json-deserializable
    deserialized = deserialize(response_text)
    # Validate the response against the Response schema (raises
    # jsonschema.ValidationError if invalid)
    if validate_against_schema:
        jsonschema.validate(deserialized, schema)
    # Batch
    if isinstance(deserialized, list):
        return [JSONRPCResponse(r) for r in deserialized if "id" in r]
    # Single request
    return JSONRPCResponse(deserialized if "id" in deserialized else None)
