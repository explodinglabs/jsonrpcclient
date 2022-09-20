from typing import Dict

import pytest

from jsonrpcclient.responses import Error, Ok, Response, parse, parse_json, to_result


def test_Ok():
    assert repr(Ok("foo", 1)) == "Ok(result='foo', id=1)"


def test_Error():
    assert (
        repr(Error(1, "foo", "bar", 2))
        == "Error(code=1, message='foo', data='bar', id=2)"
    )


@pytest.mark.parametrize(
    "argument,expected",
    [
        (
            {"jsonrpc": "2.0", "result": "foo", "id": 1},
            Ok("foo", 1),
        ),
        (
            {"jsonrpc": "2.0", "error": {"code": 1, "message": "foo"}, "id": 1},
            Error(1, "foo", None, 1),
        ),
    ],
)
def test_to_result(argument: Dict[str, str], expected: Response) -> None:
    assert to_result(argument) == expected


def test_parse():
    assert parse({"jsonrpc": "2.0", "result": "pong", "id": 1}) == Ok("pong", 1)


def test_parse_string():
    with pytest.raises(TypeError) as exc:
        parse('{"jsonrpc": "2.0", "result": "pong", "id": 1}')
    assert str(exc.value) == "Use parse_json on strings"


def test_parse_json():
    assert parse_json('{"jsonrpc": "2.0", "result": "pong", "id": 1}') == Ok("pong", 1)
