from typing import Any, Dict, Iterable, List, Union, NamedTuple

Deserialized = Union[Dict[str, Any], List[Dict[str, Any]]]


class Ok(NamedTuple):
    result: Any
    id: Any

    def __repr__(self) -> str:
        return f"Ok(result={self.result!r}, id={self.id!r})"


class Error(NamedTuple):
    code: int
    message: str
    data: Any
    id: Any

    def __repr__(self) -> str:
        return f"Error(code={self.code!r}, message={self.message!r}, data={self.data!r}, id={self.id!r})"


Response = Union[Ok, Error]


def to_result(response: Dict[str, Any]) -> Response:
    return (
        Ok(response["result"], response["id"])
        if "result" in response
        else Error(
            response["error"]["code"],
            response["error"]["message"],
            response["error"].get("data"),
            response["id"],
        )
    )


def parse(response: Deserialized) -> Union[Response, Iterable[Response]]:
    return (
        map(to_result, response) if isinstance(response, list) else to_result(response)
    )
