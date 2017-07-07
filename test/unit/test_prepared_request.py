"""test_request.py"""
from unittest import TestCase, main
from past.builtins import basestring

from jsonrpcclient.prepared_request import PreparedRequest


class TestNew(TestCase):

    def test_string(self):
        # String should remain unchanged
        req = '{"jsonrpc": "1.0", "method": "foo", "id": 1}'
        self.assertEqual(
            '{"jsonrpc": "1.0", "method": "foo", "id": 1}',
            PreparedRequest(req)
        )

    def test_dict(self):
        # Dict should convert to json-encoded string
        req = {'jsonrpc': '1.0', 'method': 'foo', 'id': 1}
        self.assertIsInstance(PreparedRequest(req), basestring)

    def test_list(self):
        # List should convert to json-encoded string
        req = [{'jsonrpc': '2.0', 'method': 'foo', 'id': 1},
               {'jsonrpc': '2.0', 'method': 'foo', 'id': 2}]
        self.assertIsInstance(PreparedRequest(req), basestring)

    def test_list_of_strings(self):
        # List of strings should convert to one json-encoded string
        req = ['{"jsonrpc": "2.0", "method": "foo", "id": 1}',
               '{"jsonrpc": "2.0", "method": "foo", "id": 2}']
        exp = '[{"jsonrpc": "2.0", "method": "foo", "id": 1}, {"jsonrpc": "2.0", "method": "foo", "id": 2}]'
        prepped = PreparedRequest(req)
        self.assertIsInstance(prepped, basestring)
        self.assertEqual(prepped, exp)


if __name__ == '__main__':
    main()
