"""
Request
*******
"""

import itertools
import json
from collections import OrderedDict

def _sort_request(req):
    """Sorts a JSON-RPC request dict returning a sorted OrderedDict, having no
    effect other than making it nicer to read.

        >>> json.dumps(_sort_request(
        ...     {'id': 2, 'params': [2, 3], 'method': 'add', 'jsonrpc': '2.0'}))
        '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 2}'

    :param req: JSON-RPC request in dict format.
    :return: The same request, nicely sorted.
    """
    sort_order = ['jsonrpc', 'method', 'params', 'id']
    return OrderedDict(sorted(req.items(), key=lambda k: sort_order.index(
        k[0])))


class Request(dict):
    """Builds a JSON-RPC request message::

        >>> Request('go', 'foo', 'bar')
        {'jsonrpc': '2.0', 'method': 'go', 'params': ['foo', 'bar']}

    Pass ``response=True`` if expecting a response::

        >>> Request('find', name='foo', response=True)
        {'jsonrpc': '2.0', 'method': 'find', 'params': {'name': 'foo'}, 'id': 1}

    :param method: The method name.
    :param args: Positional arguments.
    :param kwargs: Keyword arguments.
    :returns: The JSON-RPC request in dictionary format.
    """

    id_iterator = itertools.count(1)

    def __init__(self, method, *args, **kwargs):
        # Start the basic request
        self['jsonrpc'] = '2.0'
        self['method'] = method
        # Generate a unique id, if a response is expected
        if kwargs.get('response'):
            self['id'] = next(self.id_iterator)
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
            self['params'] = params

    def __str__(self):
        """Wrapper around request, returning a string instead of a dict"""
        return json.dumps(_sort_request(self))
