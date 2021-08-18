import json
import logging
from functools import partial
from typing import Any, Dict, Iterator

from . import id_generators
from .sentinels import NOID


def get_params(args: Any, kwargs: Any) -> Dict[str, Any]:
    return {"params": list(args) or kwargs} if (args or kwargs) else {}


def notification_dict(method: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    if args and kwargs:
        logging.warning(
            "Use positional or named arguements, but not both. This is a limitation of JSON-RPC"
        )
    return {"jsonrpc": "2.0", "method": method, **get_params(args, kwargs)}


def notification(*args: Any, **kwargs: Any) -> str:
    return json.dumps(notification_dict(*args, **kwargs))


def get_id(id: Any, id_: Any, id_generator: Iterator[Any]) -> Any:
    if id is not NOID:
        return id
    elif id_ is not NOID:
        return id_
    else:
        return next(id_generator)


def request_gen(
    id_generator: Iterator[Any],
    method: str,
    *args: Any,
    id: Any = NOID,
    id_: Any = NOID,
    **kwargs: Any,
) -> Dict[str, Any]:
    if args and kwargs:
        logging.warning(
            "Use positional or named arguements, but not both. This is a limitation of JSON-RPC"
        )
    request = {
        "jsonrpc": "2.0",
        "method": method,
        **get_params(args, kwargs),
    }
    return {**request, "id": get_id(id, id_, id_generator)}


request_natural_dict = partial(request_gen, id_generators.decimal())


def request_natural(*args: Any, **kwargs: Any) -> str:
    return json.dumps(request_natural_dict(*args, **kwargs))


request_dict = request_natural_dict
request = request_natural
