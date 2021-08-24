import json
from functools import partial
from typing import Any, Dict, Iterator, Tuple, Union

from . import id_generators
from .sentinels import NOID
from .utils import compose


def notification_dict_pure(
    method: str, params: Union[Dict[str, Any], Tuple[Any, ...]]
) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "method": method,
        **({"params": params} if params else {}),
    }


def notification_dict(
    method: str, params: Union[Dict[str, Any], Tuple[Any, ...], None] = None
) -> Dict[str, Any]:
    return notification_dict_pure(method, params if params else ())


notification = compose(json.dumps, notification_dict)


def request_pure(
    id_generator: Iterator[Any],
    method: str,
    params: Union[Dict[str, Any], Tuple[Any, ...]],
    id: Any,
) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "method": method,
        **({"params": params} if params else {}),
        "id": id if id is not NOID else next(id_generator),
    }


def request_impure(
    id_generator: Iterator[Any],
    method: str,
    params: Union[Dict[str, Any], Tuple[Any, ...], None] = None,
    id: Any = NOID,
) -> Dict[str, Any]:
    return request_pure(
        id_generator or id_generators.decimal(), method, params or (), id
    )


request_dict_natural = partial(request_impure, id_generators.decimal())
request_dict_hex = partial(request_impure, id_generators.hexadecimal())
request_dict_random = partial(request_impure, id_generators.random())
request_dict_uuid = partial(request_impure, id_generators.uuid())

request_dict = request_dict_natural
request = compose(json.dumps, request_dict_natural)
request_hex = compose(json.dumps, request_dict_hex)
request_random = compose(json.dumps, request_dict_random)
request_uuid = compose(json.dumps, request_dict_uuid)
