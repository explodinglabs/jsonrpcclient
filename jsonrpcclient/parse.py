import json
from typing import Dict, List, Optional, Union

import jsonschema  # type: ignore
from pkg_resources import resource_string

from . import exceptions
from .response import JSONRPCResponse

response_schema = json.loads(resource_string(__name__, "response-schema.json").decode())


def parse(
    response_text: str, validate_against_schema: bool = True
) -> Union[JSONRPCResponse, List[JSONRPCResponse]]:
    """
    Parses response text, returning JSONRPCResponse objects.

    :type response_text: JSON-RPC response string.
    :raises ParseResponseError: The response was not valid JSON.
    :raises ValidationError: The response was not a valid JSON-RPC response object.
    """
    if response_text:
        # If a string, ensure it's json-decodable
        try:
            decoded = json.loads(response_text)
        except ValueError:
            raise exceptions.ParseResponseError()
        # Validate the response against the Response schema (raises
        # jsonschema.ValidationError if invalid)
        if validate_against_schema:
            jsonschema.validate(decoded, response_schema)

        # Return a Response object, or a list of Responses in the case of a batch
        # request.
        if isinstance(decoded, list):
            return [JSONRPCResponse(r) for r in decoded]
        else:
            return JSONRPCResponse(decoded)
    else:
        return JSONRPCResponse(None)
