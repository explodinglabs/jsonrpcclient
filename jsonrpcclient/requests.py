import json
import logging
from functools import partial
from typing import Any, Dict, Iterator

from . import id_generators
from .sentinels import NOID
from .utils import compose


def get_params(args: Any, kwargs: Any) -> Dict[str, Any]:
    return {"params": list(args) or kwargs} if (args or kwargs) else {}


def notification_dict_pure(method: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "method": method, **get_params(args, kwargs)}


def notification_dict(method: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    if args and kwargs:
        logging.warning(
            "Use positional or named arguements, but not both. This is a limitation of JSON-RPC"
        )
    return notification_dict_pure(method, *args, **kwargs)


notification = compose(json.dumps, notification_dict)


def get_id(id: Any, id_: Any, id_generator: Iterator[Any]) -> Any:
    if id is not NOID:
        return id
    elif id_ is not NOID:
        return id_
    else:
        return next(id_generator)


def request_pure(
    id: Any,
    id_: Any,
    id_generator: Iterator[Any],
    method: str,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    return {
        **{
            "jsonrpc": "2.0",
            "method": method,
            **get_params(args, kwargs),
        },
        "id": get_id(id, id_, id_generator),
    }


def request_impure(
    id_generator: Iterator[Any],
    method: str,
    *args: Any,
    id: Any = NOID,
    id_: Any = NOID,
    **kwargs: Any,
) -> Dict[str, Any]:
    if args and kwargs:
        logging.warning(
            "Named arguments ignored. Use positional or named arguments, but not both. This is a limitation of JSON-RPC"
        )
    return request_pure(
        id, id_, id_generator or id_generators.decimal(), method, *args, **kwargs
    )


request_natural_dict = partial(request_impure, id_generators.decimal())
request_natural = compose(json.dumps, request_natural_dict)

request_dict = request_natural_dict
request = request_natural
