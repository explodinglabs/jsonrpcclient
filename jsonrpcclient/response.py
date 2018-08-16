from typing import Any, Dict, List, Optional, Union


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
        - Response.code = -32000
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

        :param response: The JSON-RPC response to process. (can be None!)
        """
        if response:
            # If the response was "error", raise to ensure it's handled
            self.id = response["id"] if "id" in response.keys() else None
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


def total_results(data, *, ok: bool = True) -> int:
    if isinstance(data, list):
        return sum([1 for d in data if d.ok == ok])
    elif isinstance(data, JSONRPCResponse):
        return int(data.ok == ok)
    else:
        return 0  # The data hasn't been parsed yet. The data attribute hasn't been set.


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
        self.data = (
            None
        )  # type: Optional[Union[JSONRPCResponse, List[JSONRPCResponse]]]

    def __repr__(self) -> str:
        total_ok = total_results(self.data, ok=True)
        total_errors = total_results(self.data, ok=False)
        if total_errors:
            return "<Response[{} ok, {} errors]>".format(total_ok, total_errors)
        else:
            return "<Response[{}]>".format(total_ok)
