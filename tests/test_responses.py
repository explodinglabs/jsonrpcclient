from jsonrpcclient.responses import Error, Ok, parse, parse_json


def test_Ok():
    assert repr(Ok("foo", 1)) == "Ok(result='foo', id=1)"


def test_Error():
    assert (
        repr(Error(1, "foo", "bar", 2))
        == "Error(code=1, message='foo', data='bar', id=2)"
    )


def test_parse():
    assert parse({"jsonrpc": "2.0", "result": "pong", "id": 1}) == Ok("pong", 1)


def test_parse_json():
    assert parse_json('{"jsonrpc": "2.0", "result": "pong", "id": 1}') == Ok("pong", 1)
