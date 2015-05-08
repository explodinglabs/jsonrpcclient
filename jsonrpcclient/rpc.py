"""rpc.py"""

import itertools
import json #pylint:disable=unused-import
from collections import OrderedDict

id_generator = itertools.count(1) # First generated is 1


def request(method, *args, **kwargs):
    #pylint:disable=line-too-long
    """Returns a JSON-RPC 2.0 request, in OrderedDict format. Convert to a json
    string with json.dumps().

    Notification
    >>> json.dumps(request('go'))
    '{"jsonrpc": "2.0", "method": "go"}'

    Passing both positional and keyword arguments
    >>> json.dumps(request('find', 'Foo', age=42))
    '{"jsonrpc": "2.0", "method": "find", "params": ["Foo", {"age": 42}]}'

    Requests (requiring a response)
    >>> json.dumps(request('add', 2, 3, response=True))
    '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}'
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
