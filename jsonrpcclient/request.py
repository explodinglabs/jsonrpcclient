"""request.py"""

import itertools
import json
from collections import OrderedDict

def hex_iterator(start=1):
    """Can be used to generate hex request ids rather than decimal.

    To use, patch id_iterator::

        >>> from jsonrpcclient import request
        >>> request.id_iterator = request.hex_iterator()
    """
    while True:
        yield '%x' % start
        start += 1

id_iterator = itertools.count(1)


def sort_request(req):
    """Sorts a JSON-RPC request dict returning a sorted OrderedDict, having no
    effect other than making it nicer to read.

        >>> json.dumps(sort_request(
        ...     {'id': 2, 'params': [2, 3], 'method': 'add', 'jsonrpc': '2.0'}))
        '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 2}'

    :param req: JSON-RPC request in dict format.
    :return: The same request, nicely sorted.
    """
    sort_order = ['jsonrpc', 'method', 'params', 'id']
    return OrderedDict(sorted(req.items(), key=lambda k: sort_order.index(
        k[0])))


def rpc_request(method, *args, **kwargs):
    """Builds a JSON-RPC request given a method name and arguments.

        >>> rpc_request('go')
        {'jsonrpc': '2.0', 'method': 'go'}

        >>> rpc_request('find', 'Foo', age=42)
        {'jsonrpc': '2.0', 'method': 'find', 'params': ['Foo', {'age': 42}]}

        >>> rpc_request('add', 2, 3, response=True)
        {'jsonrpc': '2.0', 'method': 'add', 'params': [2, 3], 'id': 2}

    :param method: The method name.
    :param args: Positional arguments.
    :param kwargs: Keyword arguments.
    :returns: The JSON-RPC request.
    """
    # Start the basic request
    req = {'jsonrpc': '2.0', 'method': method}
    # Generate a unique id, if a response is expected
    if kwargs.get('response'):
        req['id'] = next(id_iterator)
    kwargs.pop('response', None)
    # Merge the positional and named arguments into one list
    params = list()
    if args:
        params.extend(args)
    if kwargs:
        params.append(kwargs)
    if params:
        # The 'params' can be either "by-position" (a list) or "by-name" (a
        # dict). If there's only one list or dict in the params list, take it
        # out of the enclosing list, ie. [] instead of [[]], {} instead of [{}].
        if len(params) == 1 and (isinstance(params[0], dict) or \
                isinstance(params[0], list)):
            params = params[0]
        # Add the params to the request
        req['params'] = params
    return req


def rpc_request_str(method, *args, **kwargs):
    """Wrapper around rpc_request, returning a string instead of a dict"""
    return json.dumps(sort_request(rpc_request(method, *args, **kwargs)))
