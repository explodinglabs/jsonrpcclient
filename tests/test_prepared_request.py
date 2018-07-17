from jsonrpcclient.prepared_request import PreparedRequest


class TestNew():
    def test_string(self):
        # String should remain unchanged
        req = '{"jsonrpc": "1.0", "method": "foo", "id": 1}'
        assert PreparedRequest(req) == '{"jsonrpc": "1.0", "method": "foo", "id": 1}'

    def test_dict(self):
        # Dict should convert to json-encoded string
        req = {"jsonrpc": "1.0", "method": "foo", "id": 1}
        assert isinstance(PreparedRequest(req), str)

    def test_list(self):
        # List should convert to json-encoded string
        req = [
            {"jsonrpc": "2.0", "method": "foo", "id": 1},
            {"jsonrpc": "2.0", "method": "foo", "id": 2},
        ]
        assert isinstance(PreparedRequest(req), str)

    def test_list_of_strings(self):
        # List of strings should convert to one json-encoded string
        req = [
            '{"jsonrpc": "2.0", "method": "foo", "id": 1}',
            '{"jsonrpc": "2.0", "method": "foo", "id": 2}',
        ]
        exp = (
            '[{"jsonrpc": "2.0", "method": "foo", "id": 1}, {"jsonrpc": "2.0", "method": "foo", "id": 2}]'
        )
        prepped = PreparedRequest(req)
        assert isinstance(prepped, str)
        assert prepped == exp
