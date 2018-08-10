import json
import logging
from pkg_resources import resource_string
from typing import Any, Optional, Dict, Union, List

import jsonschema  # type: ignore

from . import exceptions


response_schema = json.loads(resource_string(__name__, "response-schema.json").decode())


class JSONRPCResponse:
    """
    Success response:
        - Response.ok = True
        - Response.id = 1
        - Response.result = 5
    Error response:
        - Response.ok = False
        - Response.id = 1
        - Response.message = "There was an error"
        - Response.data = None
    """

    def __init__(
        self,
        response: Optional[Dict],
        validate_against_schema: bool = True,
        log_extra: Optional[Dict] = None,
        log_format: Optional[str] = None,
        trim_log_values: bool = False,
    ) -> None:
        """
        Provides attributes representing the response.

        :param response: The JSON-RPC response to process.
        :type response: dict.
        """
        if response:
            # If the response was "error", raise to ensure it's handled
            self.id = response["id"]
            self.ok = "result" in response
            if self.ok:
                self.ok = True
                self.result = response["result"]
            else:
                self.ok = False
                self.code = response["error"].get("code")
                self.message = response["error"].get("message")
                self.data = response["error"].get("data")
        else:
            # Empty response - valid.
            self.ok = True
            self.id = None
            self.result = None

    def __repr__(self) -> str:
        if self.ok:
            return "<JSONRPCResponse(id={}, result={})>".format(self.id, self.result)
        else:
            return '<JSONRPCResponse(id={}, message="{}")>'.format(
                self.id, self.message
            )


def parse(
    response_text: str, validate_against_schema: bool = True
) -> Union[JSONRPCResponse, List[JSONRPCResponse]]:
    """
    Parses response text, returning JSONRPCResponse objects.

    :type response_text: String.
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


class Response:
    """
    Wraps a response from any client.

    >>> Response(response.text, raw=response)
    """

    def __init__(self, text: str, raw: Any = None) -> None:
        """
        :param text: The response string.
        :param raw: The client's own response object. Gives the user access to the
            client framework. (optional)
        """
        self.text = text
        self.raw = raw

    def total_results(self, *, ok: bool =True) -> int:
        if isinstance(self.data, list):
            return sum([1 for d in self.data if d.ok==ok])
        elif isinstance(self.data, JSONRPCResponse):
            return int(self.data.ok==ok)
        else:
            return 0

    def __repr__(self) -> str:
        total_ok = self.total_results(ok=True)
        total_errors = self.total_results(ok=False)
        if total_errors:
            return "<Response[{} ok, {} errors]>".format(total_ok, total_errors)
        else:
            return "<Response[{}]>".format(total_ok)

    def parse(self, validate_against_schema: bool = True) -> None:
        self.data = parse(self.text, validate_against_schema=validate_against_schema)
