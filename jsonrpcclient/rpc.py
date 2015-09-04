"""rpc.py"""

import itertools
import json #pylint:disable=unused-import

id_generator = itertools.count(1) # First generated is 1


def request(method, *args, **kwargs):
    """Builds a JSON-RPC request given a method name and arguments.

    Notification usage::

        >>> json.dumps(request('go'))
        '{"jsonrpc": "2.0", "method": "go"}'

    Passing both positional and keyword arguments::

        >>> json.dumps(request('find', 'Foo', age=42))
        '{"jsonrpc": "2.0", "method": "find", "params": ["Foo", {"age": 42}]}'

    Requests (requiring a response)::

        >>> json.dumps(request('add', 2, 3, response=True))
        '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}'

    :param method: The method name.
    :param args: List of positional arguments (optional).
    :param kwargs: Dict of keyword arguments (optional).
    :returns: The JSON-RPC request, as a dict.
    """
    # The basic request
    req = {'jsonrpc': '2.0', 'method': method}
    # Get the request id, if 'response' is passed as True. (We do this first so
    # we can then remove that key from the keyword arguments.)
    if kwargs.get('response'):
        req['id'] = next(id_generator)
    kwargs.pop('response', None)
    # Get the 'params' part. (In JSON-RPC the key is named 'params' when
    # technically they are arguments, not parameters.)
    params = list()
    if args:
        for i in args:
            params.append(i)
    if kwargs:
        params.append(kwargs)
    if params:
        # The 'params' can be either "by-position" (a list) or "by-name" (a
        # dict). If there's only one list or dict in the params list, take it
        # out of the enclosing list, ie. [] instead of [[]], {} instead of [{}].
        if len(params) == 1 and (isinstance(params[0], dict) or \
                isinstance(params[0], list)):
            params = params[0]
        req['params'] = params
    return req
