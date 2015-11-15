"""
Requests
********

These classes make it easy to create JSON-RPC Request objects.
"""

import itertools
import json
from collections import OrderedDict
from future.utils import with_metaclass

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


class _RequestClassType(type):
    """Request Metaclass.

    Purpose of this is to catch undefined attributes on the class.
    """

    def __getattr__(cls, name):
        """This gives us an alternate way to make a request::

            >>> Request.cat()
            {'jsonrpc': '2.0', 'method': 'cat', 'id': 1}

        That's the same as saying ``Request('cat')``. Technique is
        explained here: http://code.activestate.com/recipes/307618/
        """
        def attr_handler(*args, **kwargs):
            """Return the request using the specified method name."""
            return cls(name, *args, **kwargs)
        return attr_handler


class Notification(with_metaclass(_RequestClassType, dict)):
    # pylint: disable=line-too-long
    """A JSON-RPC Request object, with no ``id`` member (meaning no payload data
    is wanted)::

        >>> from jsonrpcclient import Notification
        >>> Notification('cat')
        {'jsonrpc': '2.0', 'method': 'cat'}

    The first argument is the *method*; everything else is *arguments* to the
    method::

        >>> Notification('cat', 'Mittens', 5)
        {'jsonrpc': '2.0', 'method': 'cat', params: ['Mittens', 5]}

    Keyword arguments are also acceptable::

        >>> Notification('cat', name='Mittens', age=5)
        {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens', 'age': 5}}

    If you prefer, call the method as though it was a class attribute::

        >>> Notification.cat(name='Mittens', age=5)
        {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens', 'age': 5}}

    :param method: The method name.
    :param args: Positional arguments.
    :param kwargs: Keyword arguments.
    :returns: The JSON-RPC request in dictionary form.
    """

    def __init__(self, method, *args, **kwargs):
        # Start the basic request
        self['jsonrpc'] = '2.0'
        self['method'] = method
        # Get the 'params' part
        # Merge the positional and keyword arguments into one list
        params = list()
        if args:
            params.extend(args)
        if kwargs:
            params.append(kwargs)
        if params:
            # The 'params' can be either "by-position" (a list) or "by-name" (a
            # dict). If there's only one list or dict in the params list, take
            # it out of the enclosing list, ie. [] instead of [[]], {} instead
            # of [{}].
            if len(params) == 1 and (isinstance(params[0], dict) or \
                    isinstance(params[0], list)):
                params = params[0]
            # Add the params to the request
            self['params'] = params

    def __str__(self):
        """Wrapper around request, returning a string instead of a dict"""
        return json.dumps(_sort_request(self))


class Request(Notification):
    """A JSON-RPC Request object, with an ``id`` member (meaning payload data is
    wanted)::

        >>> Request('cat')
        {'jsonrpc': '2.0', 'method': 'cat', 'id': 1}

    An auto-incremented ``id`` is used, so each request has a unique ``id``::

        >>> Request('cat')
        {'jsonrpc': '2.0', 'method': 'cat', 'id': 2}

    Use ``request_id`` to specify the ``id`` to use::

        >>> Request('cat', request_id='Request #1')
        {'jsonrpc': '2.0', 'method': 'cat', 'id': 'Request #1'}

    :param method: The method name.
    :param args: Positional arguments.
    :param kwargs: Keyword arguments.
    :returns: The JSON-RPC request in dictionary form.
    """

    id_iterator = itertools.count(1)

    def __init__(self, method, *args, **kwargs):
        # 'response' means use an auto-iterated id
        #kwargs.pop('response', None)
        # 'request_id' means use the specified id
        if kwargs.get('request_id'):
            self['id'] = kwargs['request_id']
        else:
            self['id'] = next(self.id_iterator)
        kwargs.pop('request_id', None)
        super(Request, self).__init__(method, *args, **kwargs)
