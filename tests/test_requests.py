from jsonrpcclient import id_generators
from jsonrpcclient.requests import Notification, Request


class TestNotification:
    def test(self):
        assert Notification("get") == {"jsonrpc": "2.0", "method": "get"}

    def test_str(self):
        assert str(Notification("get")) == '{"jsonrpc": "2.0", "method": "get"}'

    def test_method_name_directly(self):
        assert {"jsonrpc": "2.0", "method": "cat"} == Notification.cat()

    def test_positional(self):
        assert Notification("sqrt", 1) == {
            "jsonrpc": "2.0",
            "method": "sqrt",
            "params": [1],
        }
        assert Notification("sqrt", [1, 2, 3]) == {
            "jsonrpc": "2.0",
            "method": "sqrt",
            "params": [[1, 2, 3]],
        }
        assert Notification("sqrt", {"name": "Foo"}) == {
            "jsonrpc": "2.0",
            "method": "sqrt",
            "params": [{"name": "Foo"}],
        }

    def test_keyword(self):
        assert Notification("find", name="Foo") == {
            "jsonrpc": "2.0",
            "method": "find",
            "params": {"name": "Foo"},
        }

    def test_both(self):
        assert Notification("find", "Foo", age=42) == {
            "jsonrpc": "2.0",
            "method": "find",
            "params": ["Foo", {"age": 42}],
        }


class TestRequest:
    def setup_method(self):
        # Reset the id generator, to start the ids at 1
        Request.id_generator = id_generators.decimal()

    def test(self):
        assert Request("get") == {"jsonrpc": "2.0", "method": "get", "id": 1}

    def test_str(self):
        assert str(Request("get")) == '{"jsonrpc": "2.0", "method": "get", "id": 1}'

    def test_method_name_directly(self):
        assert Request.cat() == {"jsonrpc": "2.0", "method": "cat", "id": 1}

    def test_positional(self):
        assert Request("sqrt", 1) == {
            "jsonrpc": "2.0",
            "method": "sqrt",
            "params": [1],
            "id": 1,
        }
        assert Request("sqrt", [1, 2, 3]) == {
            "jsonrpc": "2.0",
            "method": "sqrt",
            "params": [[1, 2, 3]],
            "id": 2,
        }
        assert Request("sqrt", {"name": "Foo"}) == {
            "jsonrpc": "2.0",
            "method": "sqrt",
            "params": [{"name": "Foo"}],
            "id": 3,
        }

    def test_keyword(self):
        assert Request("find", name="Foo") == {
            "jsonrpc": "2.0",
            "method": "find",
            "params": {"name": "Foo"},
            "id": 1,
        }

    def test_auto_iterating_id(self):
        assert Request("go") == {"jsonrpc": "2.0", "method": "go", "id": 1}
        assert Request("go") == {"jsonrpc": "2.0", "method": "go", "id": 2}

    def test_specified_id(self):
        assert Request("get", request_id="Request #1") == {
            "jsonrpc": "2.0",
            "method": "get",
            "id": "Request #1",
        }

    def test_custom_iterator(self):
        req = Request("go", id_generator=id_generators.random())
        assert len(req["id"]) == 8
