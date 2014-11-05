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
# pylint: disable=missing-docstring,line-too-long

import json
from nose.tools import assert_equal # pylint: disable=no-name-in-module

from . import rpc

# Notifications

def test_method_only():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "go"}',
        json.dumps(rpc.request('go'))
    )

def test_one_arg():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "print", "params": ["Hello world"]}',
        json.dumps(rpc.request('print', 'Hello world'))
    )

def test_two_args():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "print", "params": ["Hello", "world"]}',
        json.dumps(rpc.request('print', 'Hello', 'world'))
    )

def test_one_kwarg():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "print", "params": {"string": "Hello world"}}',
        json.dumps(rpc.request('print', string='Hello world'))
    )

def test_two_kwargs():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "print", "params": {"string1": "Hello", "string2": "world"}}',
        json.dumps(rpc.request('print', string1='Hello', string2='world'))
    )

def test_args_and_kwargs():
    # Both args and kwargs

    assert_equal(
        '{"jsonrpc": "2.0", "method": "set_age", "params": [40, {"name": "Beau Barker"}]}',
        json.dumps(rpc.request('set_age', 40, name='Beau Barker'))
    )

def test_multiple_args_and_kwargs():
    # Both args and kwargs

    assert_equal(
        '{"jsonrpc": "2.0", "method": "set_age", "params": [39, 40, {"first": "Beau", "last": "Barker"}]}',
        json.dumps(rpc.request('set_age', 39, 40, first='Beau', last='Barker'))
    )

# Non-notifications (require a response)

def test_method_only_request():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "get", "id": 1}',
        json.dumps(rpc.request('get', response=True))
    )

def test_one_arg_request():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "sqrt", "params": [1], "id": 2}',
        json.dumps(rpc.request('sqrt', 1, response=True))
    )

def test_two_args_request():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 3}',
        json.dumps(rpc.request('add', 1, 2, response=True))
    )

def test_one_kwarg_request():

    assert_equal(
        '{"jsonrpc": "2.0", "method": "find", "params": {"name": "Beau"}, "id": 4}',
        json.dumps(rpc.request('find', name='Beau', response=True))
    )

def test_two_kwargs_request():
    # Note in the resulting json, the params are in reverse order to how the
    # kwargs are called, because the args are sorted by key in the request
    # function. This is the only way to know exactly how the request will look
    # because the kwargs come in a random order. There is no way of getting the
    # actual order of the kwargs

    assert_equal(
        '{"jsonrpc": "2.0", "method": "find", "params": {"age": 38, "name": "Beau"}, "id": 5}',
        json.dumps(rpc.request('find', name='Beau', age=38, response=True))
    )

def test_args_and_kwargs_request():
    # Includes both args and kwargs

    assert_equal(
        '{"jsonrpc": "2.0", "method": "find", "params": {"age": 38, "name": "Beau"}, "id": 6}',
        json.dumps(rpc.request('find', name='Beau', age=38, response=True))
    )

def test_multiple_args_and_kwargs_request():
    # Both args and kwargs

    assert_equal(
        '{"jsonrpc": "2.0", "method": "set_age", "params": [39, 40, {"first": "Beau", "last": "Barker"}], "id": 7}',
        json.dumps(rpc.request('set_age', 39, 40, first='Beau', last='Barker', response=True))
    )
