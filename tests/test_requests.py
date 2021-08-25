from jsonrpcclient.requests import (
    notification,
    notification_json,
    request,
    request_json,
)


def test_notification():
    assert notification("get") == {"jsonrpc": "2.0", "method": "get"}


def test_notification_positional():
    assert notification("sqrt", params=[1]) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [1],
    }
    assert notification("sqrt", params=[1, 2, 3]) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [1, 2, 3],
    }
    assert notification("sqrt", params={"name": "Foo"}) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": {"name": "Foo"},
    }


def test_notification_keyword():
    assert notification("find", params={"name": "Foo"}) == {
        "jsonrpc": "2.0",
        "method": "find",
        "params": {"name": "Foo"},
    }


def test_notification_json():
    assert notification_json("foo") == '{"jsonrpc": "2.0", "method": "foo"}'


def test_request():
    assert request("foo", id=1) == {"jsonrpc": "2.0", "method": "foo", "id": 1}


def test_request_positional():
    assert request("sqrt", params=[1], id=1) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [1],
        "id": 1,
    }
    assert request("sqrt", params=[1, 2, 3], id=2) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [1, 2, 3],
        "id": 2,
    }
    assert request("sqrt", params={"name": "Foo"}, id=3) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": {"name": "Foo"},
        "id": 3,
    }


def test_request_keyword():
    assert request("foo", {"name": "bar"}, id=1) == {
        "jsonrpc": "2.0",
        "method": "foo",
        "params": {"name": "bar"},
        "id": 1,
    }


def test_request_auto_iterating_id():
    assert request("foo") == {"jsonrpc": "2.0", "method": "foo", "id": 1}
    assert request("foo") == {"jsonrpc": "2.0", "method": "foo", "id": 2}


def test_request_json():
    assert request_json("foo", id=1) == '{"jsonrpc": "2.0", "method": "foo", "id": 1}'
