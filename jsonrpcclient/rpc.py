"""rpc.py"""

import itertools
import json #pylint:disable=unused-import
from collections import OrderedDict

id_generator = itertools.count(1) # First generated is 1


def request(method, *args, **kwargs):
    #pylint:disable=line-too-long
    """Returns a JSON-RPC 2.0 request, in OrderedDict format. Convert to a json
    string with json.dumps().

    Notifications:

    No arguments
    >>> json.dumps(request('get'))
    '{"jsonrpc": "2.0", "method": "get"}'

    One positional
    >>> json.dumps(request('sqrt', 1))
    '{"jsonrpc": "2.0", "method": "sqrt", "params": [1]}'

    Two positional
    >>> json.dumps(request('add', 1, 2))
    '{"jsonrpc": "2.0", "method": "add", "params": [1, 2]}'

    One keyword
    >>> json.dumps(request('find', name='Foo'))
    '{"jsonrpc": "2.0", "method": "find", "params": {"name": "Foo"}}'

    Two keywords
    Note that keyword arguments are sorted in alphabetical order by the keys.
    This is because they're not received in any order, so we sort them, to be
    sure of *some* order
    >>> json.dumps(request('find', name='Foo', age=42))
    '{"jsonrpc": "2.0", "method": "find", "params": {"age": 42, "name": "Foo"}}'

    Both positional and keyword
    >>> json.dumps(request('find', 'Foo', age=42))
    '{"jsonrpc": "2.0", "method": "find", "params": ["Foo", {"age": 42}]}'

    Dict
    >>> json.dumps(request('find', name='Foo', age=42))
    '{"jsonrpc": "2.0", "method": "find", "params": {"age": 42, "name": "Foo"}}'

    List
    >>> json.dumps(request('find', ['Foo', 42]))
    '{"jsonrpc": "2.0", "method": "find", "params": ["Foo", 42]}'

    Requests (requiring a response):

    >>> json.dumps(request('go', response=True))
    '{"jsonrpc": "2.0", "method": "go", "id": 1}'

    >>> json.dumps(request('go', 'positional', keyword='foo', response=True))
    '{"jsonrpc": "2.0", "method": "go", "params": ["positional", {"keyword": "foo"}], "id": 2}'
    """

    # Get the request id
    request_id = None
    if kwargs.get('response', False):
        request_id = next(id_generator)

    # Pop 'response' out of the kwargs if present
    if 'response' in kwargs:
        kwargs.pop('response')


    # jsonrpc, method
    r = OrderedDict([
        ('jsonrpc', '2.0'),
        ('method', method)
    ])


    # Get the params
    params = list()

    if args:
        for i in args:
            params.append(i)

    if kwargs:
        params.append(OrderedDict(sorted(kwargs.items())))

    if len(params):

        # If there's only param and it's a dict or list, take it out of the
        # params list, rather than having a list within a list [[]]
        if len(params) == 1 and (
                isinstance(params[0], dict) or isinstance(params[0], list)):
            params = params[0]

        r.update(OrderedDict([
            ('params', params)
        ]))


    # response_id
    if request_id:
        r.update(OrderedDict([
            ('id', request_id)
        ]))

    return r
