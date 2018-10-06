"""
Classes to help create JSON-RPC Request objects.

Named plural to distinguish it from the request convenience function.

To create a request:

    >>> Request("cat", name="Yoko")
    {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Yoko'}, 'id': 1}
"""
import json
from collections import OrderedDict
from typing import Any, Callable, Dict, Iterator, List, Optional

from . import id_generators


def sort_request(request: Dict[str, Any]) -> OrderedDict:
    """
    Sort a JSON-RPC request dict.

    This has no effect other than making the request nicer to read.

        >>> json.dumps(sort_request(
        ...     {'id': 2, 'params': [2, 3], 'method': 'add', 'jsonrpc': '2.0'}))
        '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 2}'

    Args:
        request: JSON-RPC request in dict format.
    """
    sort_order = ["jsonrpc", "method", "params", "id"]
    return OrderedDict(sorted(request.items(), key=lambda k: sort_order.index(k[0])))


class _RequestClassType(type):
    """
    Request Metaclass.

    Catches undefined attributes on the class.
    """

    def __getattr__(cls: Callable, name: str) -> Callable:
        """
        This gives us an alternate way to make a request:

        >>> Request.cat()
        {'jsonrpc': '2.0', 'method': 'cat', 'id': 1}

        That's the same as saying `Request("cat")`.
        """

        def attr_handler(*args: Any, **kwargs: Any) -> "Request":
            return cls(name, *args, **kwargs)

        return attr_handler


class Notification(dict, metaclass=_RequestClassType):  # type: ignore
    """
    A request which does not expect a response.

    >>> Notification("cat")
    {'jsonrpc': '2.0', 'method': 'cat'}

    The first argument is the *method*; everything else is *arguments* to the
    method:

    >>> Notification("cat", 'Yoko', 5)
    {'jsonrpc': '2.0', 'method': 'cat', params: ['Yoko', 5]}

    Keyword arguments are also acceptable:

    >>> Notification("cat", name="Yoko", age=5)
    {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Yoko', 'age': 5}}

    If you prefer, call the method as though it was a class attribute:

    >>> Notification.cat(name="Yoko", age=5)
    {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Yoko', 'age': 5}}

    Args:
        method: The method name.
        args: Positional arguments.
        kwargs: Keyword arguments.

    Returns:
        The JSON-RPC request in dictionary form.
    """

    def __init__(self, method: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(jsonrpc="2.0", method=method)
        # Build the 'params' part. Merge the positional and keyword arguments into one
        # list.
        params_list = []  # type: List
        if args:
            params_list.extend(args)
        if kwargs:
            params_list.append(kwargs)
        # Add the params to self.
        if params_list:
            # The 'params' can be either "by-position" (a list) or "by-name" (a dict).
            # If there's only one list or dict in the params list, take it out of the
            # enclosing list, ie. [] instead of [[]], {} instead of [{}].
            if len(params_list) == 1 and (isinstance(params_list[0], (dict, list))):
                self.update(params=params_list[0])
            else:
                self.update(params=params_list)

    def __str__(self) -> str:
        """Wrapper around request, returning a string instead of a dict"""
        return json.dumps(sort_request(self))


class Request(Notification):
    """
    Create a JSON-RPC request object
    http://www.jsonrpc.org/specification#request_object.

    >>> Request("cat", name="Yoko")
    {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Yoko'}, 'id': 1}

    Args:
        method: The `method` name.
        args: Positional arguments added to `params`.
        kwargs: Keyword arguments added to `params`. Use request_id=x to force the
            `id` to use.

    Returns:
        The JSON-RPC request in dictionary form.
    """

    id_generator = id_generators.decimal()

    def __init__(
        self,
        method: str,
        *args: Any,
        id_generator: Optional[Iterator[Any]] = None,
        **kwargs: Any
    ) -> None:
        # If 'request_id' is passed, use the specified id
        if "request_id" in kwargs:
            id_ = kwargs.pop("request_id", None)
        else:  # Get the next id from the generator
            id_generator = (
                id_generator if id_generator is not None else self.id_generator
            )
            id_ = next(id_generator)
        # We call super last, after popping the request_id
        super().__init__(method, *args, **kwargs)
        self.update(id=id_)
