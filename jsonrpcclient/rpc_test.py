# pylint: disable=missing-docstring,line-too-long
"""rpc_test.py

This should test:

Notifications
    rpc.request('go')
    rpc.request('print', 'Hello world')
    rpc.request('print', 'Hello', 'world')
    rpc.request('print', string='Hello world')
    rpc.request('print', string1='Hello', string2='world')
    rpc.request('set_age', 40, name='Beau Barker')

Requests (requiring a response):
    rpc.request('get', response=True)
    rpc.request('sqrt', 1, response=True)
    rpc.request('add', 1, 2, response=True)
    rpc.request('find', name='Beau', response=True)
    rpc.request('find', name='Beau', age=38, response=True)
    rpc.request('set_age', 40, name="Beau Barker", response=True)
"""

import unittest
import itertools
from nose.tools import assert_equal # pylint: disable=no-name-in-module

from . import rpc

class RPCTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods,no-self-use

    def setUp(self):
        rpc.id_generator = itertools.count(1) # First generated is 1

    # Notifications

    def test_method_only(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "go"},
            rpc.request('go')
        )

    def test_one_arg(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "print", "params": ["Hello world"]},
            rpc.request('print', 'Hello world')
        )

    def test_two_args(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "print", "params": ["Hello", "world"]},
            rpc.request('print', 'Hello', 'world')
        )

    def test_one_kwarg(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "print", "params": {"string": "Hello world"}},
            rpc.request('print', string='Hello world')
        )

    def test_two_kwargs(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "print", "params": {"string1": "Hello", "string2": "world"}},
            rpc.request('print', string1='Hello', string2='world')
        )

    def test_args_and_kwargs(self):
        """Both args and kwargs"""

        assert_equal(
            {"jsonrpc": "2.0", "method": "set_age", "params": [40, {"name": "Beau Barker"}]},
            rpc.request('set_age', 40, name='Beau Barker')
        )

    def test_multiple_args_and_kwargs(self):
        """Both args and kwargs"""

        assert_equal(
            {"jsonrpc": "2.0", "method": "set_age", "params": [39, 40, {"first": "Beau", "last": "Barker"}]},
            rpc.request('set_age', 39, 40, first='Beau', last='Barker')
        )

# Non-notifications (require a response)

    def test_method_only_request(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "get", "id": 1},
            rpc.request('get', response=True)
        )

    def test_one_arg_request(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "sqrt", "params": [1], "id": 1},
            rpc.request('sqrt', 1, response=True)
        )

    def test_two_args_request(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1},
            rpc.request('add', 1, 2, response=True)
        )

    def test_one_kwarg_request(self):
        assert_equal(
            {"jsonrpc": "2.0", "method": "find", "params": {"name": "Beau"}, "id": 1},
            rpc.request('find', name='Beau', response=True)
        )

    def test_two_kwargs_request(self):
        # Note in the resulting json, the params are in reverse order to how the
        # kwargs are called, because the args are sorted by key in the request
        # function. This is the only way to know exactly how the request will look
        # because the kwargs come in a random order. There is no way of getting the
        # actual order of the kwargs
        assert_equal(
            {"jsonrpc": "2.0", "method": "find", "params": {"age": 38, "name": "Beau"}, "id": 1},
            rpc.request('find', name='Beau', age=38, response=True)
        )

    def test_args_and_kwargs_request(self):
        # Includes both args and kwargs
        assert_equal(
            {"jsonrpc": "2.0", "method": "find", "params": {"age": 38, "name": "Beau"}, "id": 1},
            rpc.request('find', name='Beau', age=38, response=True)
        )

    def test_multiple_args_and_kwargs_request(self):
        # Both args and kwargs
        assert_equal(
            {"jsonrpc": "2.0", "method": "set_age", "params": [39, 40, {"first": "Beau", "last": "Barker"}], "id": 1},
            rpc.request('set_age', 39, 40, first='Beau', last='Barker', response=True)
        )
