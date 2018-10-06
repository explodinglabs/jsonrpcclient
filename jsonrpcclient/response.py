"""
Response and JSONRPCResponse classes.

This module needs a major overhaul.
"""
from collections import OrderedDict
from json import dumps as serialize
from typing import Any, Dict, List, Union

NOID = object()


def sort_response(response: Dict[str, Any]) -> OrderedDict:
    """
    Sort the keys in a JSON-RPC response object.

    This has no effect other than making it nicer to read. Useful in Python 3.5 only,
    dictionaries are already sorted in newer Python versions.

    Example::

        >>> json.dumps(sort_response({'id': 2, 'result': 5, 'jsonrpc': '2.0'}))
        {"jsonrpc": "2.0", "result": 5, "id": 1}

    Args:
        response: Deserialized JSON-RPC response.

    Returns:
        The same response, sorted in an OrderedDict.
    """
    root_order = ["jsonrpc", "result", "error", "id"]
    error_order = ["code", "message", "data"]
    req = OrderedDict(sorted(response.items(), key=lambda k: root_order.index(k[0])))
    if "error" in response:
        req["error"] = OrderedDict(
            sorted(response["error"].items(), key=lambda k: error_order.index(k[0]))
        )
    return req


class JSONRPCResponse:
    """
    A parsed JSON-RPC response object.

    Base class for the responses. There should be no need to validate the input data to
    these responses, since the data hass passed the jsonschema validation.
    """

    ok = False

    def __init__(self, jsonrpc: str, id: Any) -> None:
        self.jsonrpc = jsonrpc
        self.id = id


class SuccessResponse(JSONRPCResponse):
    """
    Represents a JSON-RPC success response object.
    """

    ok = True

    def __init__(self, result: Any, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.result = result

    def __repr__(self) -> str:
        return "<SuccessResponse(id={}, result={})>".format(self.id, self.result)

    def __str__(self) -> str:
        return serialize(
            sort_response(dict(jsonrpc=self.jsonrpc, result=self.result, id=self.id))
        )


class NotificationResponse(SuccessResponse):
    """
    Represents a JSON-RPC notification response object.
    """

    ok = True

    def __init__(self) -> None:
        super().__init__(jsonrpc="2.0", result=None, id=NOID)

    def __repr__(self) -> str:
        return "<NotificationResponse()>"

    def __str__(self) -> str:
        return ""


class ErrorResponse(JSONRPCResponse):
    """
    Represents a JSON-RPC error response object.
    """

    ok = False

    def __init__(self, error: Dict[str, Any], **kwargs: Any) -> None:
        super().__init__(id=kwargs.pop("id", NOID), **kwargs)
        self.message = error.get("message")
        self.code = error.get("code")
        self.data = error.get("data")

    def __repr__(self) -> str:
        if self.id is NOID:
            return '<ErrorResponse(message="{}")>'.format(self.message)
        return '<ErrorResponse(id={}, message="{}")>'.format(self.id, self.message)

    def __str__(self) -> str:
        error = dict(code=self.code, message=self.message)
        if self.data:
            error["data"] = self.data
        deserialized = dict(jsonrpc=self.jsonrpc, error=error)
        if self.id is not NOID:
            deserialized["id"] = self.id
        return serialize(sort_response(deserialized))


def total_results(
    data: Union[List[JSONRPCResponse], JSONRPCResponse, None], *, ok: bool = True
) -> int:
    """
    Returns the total parsed responses, given the return value from parse().
    """
    if isinstance(data, list):
        return sum([1 for d in data if d.ok == ok])
    elif isinstance(data, JSONRPCResponse):
        return int(data.ok == ok)
    return 0  # The data hasn't been parsed yet. The data attribute hasn't been set.


class Response:
    """
    Wraps a client response.

    >>> Response(response.text, raw=response)
    """

    def __init__(self, text: str, raw: Any = None) -> None:
        """
        Args:
            text: The response string, as it was returned from the server.
            raw: The framework's own response object. Gives the user access to the
                framework (e.g. Requests library's `Response` object). (optional)
        """
        self.text = text
        self.raw = raw
        # Data is the parsed version of the response.
        self.data = None  # type: Union[JSONRPCResponse, List[JSONRPCResponse], None]

    def __repr__(self) -> str:
        total_ok = total_results(self.data, ok=True)
        total_errors = total_results(self.data, ok=False)
        if total_errors:
            return "<Response[{} ok, {} errors]>".format(total_ok, total_errors)
        return "<Response[{}]>".format(total_ok)
