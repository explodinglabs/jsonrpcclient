"""test_request.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main
import itertools
import json

from jsonrpcclient import request
from jsonrpcclient.request import Request, _sort_request


class TestRPC(TestCase):

    def setUp(self):
        # Ensure we start each test with id 1
        request.id_iterator = itertools.count(1)


class TestSortRequest(TestRPC):

    def test(self):
        self.assertEqual(
            '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 2}',
            json.dumps(_sort_request({'id': 2, 'params': [2, 3], 'method': 'add', 'jsonrpc': '2.0'})),
        )


class TestNotifications(TestRPC):

    def test_no_arguments(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'get'},
            Request('get')
        )

    def test_one_positional(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'sqrt', 'params': [1]},
            Request('sqrt', 1)
        )

    def test_two_positionals(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'add', 'params': [1, 2]},
            Request('add', 1, 2)
        )

    def test_one_keyword(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': {'name': 'Foo'}},
            Request('find', name='Foo')
        )

    def test_two_keywords(self):
        """Note that keyword arguments are sorted in alphabetical order by the
        keys. This is because they're not received in any order, so we sort
        them, to be sure of *some* order
        """
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': {'age': 42, 'name': 'Foo'}},
            Request('find', name='Foo', age=42)
        )

    def test_both_positional_and_keyword(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': ['Foo', {'age': 42}]},
            Request('find', 'Foo', age=42)
        )

    def test_dict_params(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': {'age': 42, 'name': 'Foo'}},
            Request('find', name='Foo', age=42)
        )

    def test_list_params(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': ['Foo', 42]},
            Request('find', ['Foo', 42])
        )


class TestRequests(TestRPC):

    def test_method_only_requiring_response(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'id': 1},
            Request('go', response=True)
        )

    def test_both_positional_and_keyword_requiring_response(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'params': ['positional', {'keyword': 'foo'}], 'id': 1},
            Request('go', 'positional', keyword='foo', response=True)
        )

    def test_incremental_id(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'id': 1},
            Request('go', response=True)
        )
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'id': 2},
            Request('go', response=True)
        )

    def test_custom_generator(self):
        standard_generator = request.id_iterator
        request.id_iterator = request.hex_iterator()
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'id': '1'},
            Request('go', response=True)
        )
        # Restore
        request.id_iterator = standard_generator

    def test_str(self):
        self.assertEqual(
            '{"jsonrpc": "2.0", "method": "get"}',
            str(Request('get'))
        )


if __name__ == '__main__':
    main()
