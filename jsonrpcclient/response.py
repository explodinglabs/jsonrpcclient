from typing import Any, List, Optional, Union

from .parse import JSONRPCResponse


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

    def total_results(self, *, ok: bool = True) -> int:
        if isinstance(self.data, list):
            return sum([1 for d in self.data if d.ok == ok])
        elif isinstance(self.data, JSONRPCResponse):
            return int(self.data.ok == ok)
        else:
            # The data hasn't been parsed yet, the data attribute has not been set.
            return 0

    def __repr__(self) -> str:
        total_ok = self.total_results(ok=True)
        total_errors = self.total_results(ok=False)
        if total_errors:
            return "<Response[{} ok, {} errors]>".format(total_ok, total_errors)
        else:
            return "<Response[{}]>".format(total_ok)
