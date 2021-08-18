from jsonrpcclient.requests import notification_dict, notification, request_dict


def test_notification_dict():
    assert notification_dict("get") == {"jsonrpc": "2.0", "method": "get"}


def test_notification_dict_positional():
    assert notification_dict("sqrt", 1) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [1],
    }
    assert notification_dict("sqrt", [1, 2, 3]) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [[1, 2, 3]],
    }
    assert notification_dict("sqrt", {"name": "Foo"}) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [{"name": "Foo"}],
    }


def test_notification_keyword():
    assert notification_dict("find", name="Foo") == {
        "jsonrpc": "2.0",
        "method": "find",
        "params": {"name": "Foo"},
    }


def test_notification_both():
    assert notification_dict("find", "Foo", age=42) == {
        "jsonrpc": "2.0",
        "method": "find",
        "params": ["Foo"],  # Ignores kwargs
    }


def test_notification():
    assert notification("foo") == '{"jsonrpc": "2.0", "method": "foo"}'


def test_request_dict():
    assert request_dict("foo", id=1) == {"jsonrpc": "2.0", "method": "foo", "id": 1}


def test_request_dict_positional():
    assert request_dict("sqrt", 1, id=1) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [1],
        "id": 1,
    }
    assert request_dict("sqrt", [1, 2, 3], id=2) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [[1, 2, 3]],
        "id": 2,
    }
    assert request_dict("sqrt", {"name": "Foo"}, id=3) == {
        "jsonrpc": "2.0",
        "method": "sqrt",
        "params": [{"name": "Foo"}],
        "id": 3,
    }


def test_request_dict_keyword():
    assert request_dict("foo", name="bar", id=1) == {
        "jsonrpc": "2.0",
        "method": "foo",
        "params": {"name": "bar"},
        "id": 1,
    }


def test_request_dict_auto_iterating_id():
    assert request_dict("foo") == {"jsonrpc": "2.0", "method": "foo", "id": 1}
    assert request_dict("foo") == {"jsonrpc": "2.0", "method": "foo", "id": 2}
