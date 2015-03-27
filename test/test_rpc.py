"""test_rpc.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main
import itertools

from jsonrpcclient import rpc


class TestRPC(TestCase):

    def setUp(self):
        rpc.id_generator = itertools.count(1) # First generated is 1

    # Notifications

    def test_no_arguments(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "get"},
            rpc.request('get')
        )

    def test_one_positional(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "sqrt", "params": [1]},
            rpc.request('sqrt', 1)
        )

    def test_two_positionals(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "add", "params": [1, 2]},
            rpc.request('add', 1, 2)
        )

    def test_one_keyword(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": {"name": "Foo"}},
            rpc.request('find', name='Foo')
        )

    def test_two_keywords(self):
        """Note that keyword arguments are sorted in alphabetical order by the
        keys. This is because they're not received in any order, so we sort
        them, to be sure of *some* order"""
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": {"age": 42, "name": "Foo"}},
            rpc.request('find', name='Foo', age=42)
        )

    def test_both_positional_and_keyword(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": ["Foo", {"age": 42}]},
            rpc.request('find', 'Foo', age=42)
        )

    def test_dict_params(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": {"age": 42, "name": "Foo"}},
            rpc.request('find', name='Foo', age=42)
        )

    def test_list_params(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": ["Foo", 42]},
            rpc.request('find', ['Foo', 42])
        )

    # Requests (requiring a response)

    def test_request_method_only(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "go", "id": 1},
            rpc.request('go', response=True)
        )

    def test_request_both_positional_and_keyword(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "go", "params": ["positional", {"keyword": "foo"}], "id": 1},
            rpc.request('go', 'positional', keyword='foo', response=True)
        )

if __name__ == '__main__':
    main()
