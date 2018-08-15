from jsonrpcclient.parse import parse
from jsonrpcclient.response import JSONRPCResponse, Response, total_results


class TestTotalResults:
    def test_unparsed(self):
        assert total_results(None) == 0

    def test_one(self):
        res = {"jsonrpc": "2.0", "result": "foo", "id": 1}
        jsonrpc_response = JSONRPCResponse(res)
        assert total_results(jsonrpc_response) == 1

    def test_list(self):
        res = {"jsonrpc": "2.0", "result": "foo", "id": 1}
        jsonrpc_response = JSONRPCResponse(res)
        assert total_results([jsonrpc_response, jsonrpc_response]) == 2


class TestResponse:
    def test(self):
        response = Response("foo")
        assert response.text == "foo"

    def test_repr(self):
        response = Response("foo")
        assert repr(response) == "<Response[0]>"

    def test_repr_with_results(self):
        response = Response("foo")
        response.data = JSONRPCResponse(
            {"jsonrpc": "2.0", "error": {"message": "foo"}, "id": 1}
        )
        assert repr(response) == "<Response[0 ok, 1 errors]>"
