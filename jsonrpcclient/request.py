"""request.py"""

import itertools
import json
from collections import OrderedDict
from uuid import uuid4
from string import digits, ascii_lowercase
from random import choice

def hex_iterator(start=1):
    """Use incremental request ids in hexadecimal rather than decimal format::

        >>> from jsonrpcclient import Request, hex_iterator
        >>> Request.id_iterator = hex_iterator()
    """
    while True:
        yield '%x' % start
        start += 1


def uuid_iterator():
    """Use unique uuid ids rather incremental decimal::

        >>> from jsonrpcclient import Request, hex_iterator
        >>> Request.id_iterator = uuid_iterator()
    """
    while True:
        yield str(uuid4())


def random_iterator(length=8, chars=digits+ascii_lowercase):
    """Use a random string. Has possible collisions - with default values
    probability is around 1 in a million::

        >>> from jsonrpcclient import Request, shortuuid_iterator
        >>> Request.id_iterator = random_iterator()
    """
    while True:
        yield ''.join([choice(chars) for i in range(length)])


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

    id_iterator = itertools.count(1)

    def __init__(self, method, *args, **kwargs):
        """Builds a JSON-RPC request given a method name and arguments.

            >>> Request('go')
            {'jsonrpc': '2.0', 'method': 'go'}

            >>> Request('find', 'Foo', age=42)
            {'jsonrpc': '2.0', 'method': 'find', 'params': ['Foo', {'age': 42}]}

            >>> Request('add', 2, 3, response=True)
            {'jsonrpc': '2.0', 'method': 'add', 'params': [2, 3], 'id': 2}

        :param method: The method name.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :returns: The JSON-RPC request.
        """
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
