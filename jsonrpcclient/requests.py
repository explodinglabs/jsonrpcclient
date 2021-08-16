import json
from typing import Any, Callable, Iterator, Optional

from . import id_generators


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
        # Add the params to self.
        if args and kwargs:
            # The 'params' can be *EITHER* "by-position" (a list) or "by-name" (a dict).
            # Therefore, in this case it violates the JSON-RPC 2.0 specification.
            # However, it provides the same behavior as the previous version of
            # jsonrpcclient to keep compatibility.
            # TODO: consider to raise a warning.
            params_list = list(args)
            params_list.append(kwargs)
            self.update(params=params_list)
        elif args:
            self.update(params=list(args))
        elif kwargs:
            self.update(params=kwargs)

    def __str__(self) -> str:
        """Wrapper around request, returning a string instead of a dict"""
        return json.dumps(self)


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
