from json import JSONDecodeError

import pytest
from jsonschema import ValidationError

from jsonrpcclient.parse import parse


def test_parse():
    parse('{"jsonrpc": "2.0", "result": "foo", "id": 1}', batch=False)


def test_parse_invalid_json():
    with pytest.raises(JSONDecodeError):
        parse("{dodgy}", batch=False)


def test_parse_invalid_jsonrpc():
    with pytest.raises(ValidationError):
        parse('{"json": "2.0"}', batch=False)


def test_parse_without_validation():
    parse(
        '{"jsonrpc": "2.0", "result": "foo", "id": 1}',
        batch=False,
        validate_against_schema=False,
    )


def test_parse_batch():
    data = parse('[{"jsonrpc": "2.0", "result": "foo", "id": 1}]', batch=True)
    assert data[0].result == "foo"


def test_parse_batch_ignores_notifications():
    data = parse('[{"jsonrpc": "2.0", "result": "foo", "id": 1}]', batch=True)
    assert len(data) == 1


def test_parse_empty_string_single():
    assert parse("", batch=False).result is None


def test_parse_empty_string_batch():
    assert parse("", batch=True) == []


def test_parse_none_single():
    assert parse(None, batch=False).result is None


def test_parse_none_batch():
    assert parse(None, batch=True) == []
