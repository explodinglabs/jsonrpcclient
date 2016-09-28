"""These classes make it easy to create JSON-RPC Request objects."""

import json
from collections import OrderedDict
from future.utils import with_metaclass

from . import config, ids


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
    #pylint:enable=line-too-long

    def __init__(self, method, *args, **kwargs):
        # Start the basic request
        self.update(jsonrpc='2.0', method=method)
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
            self.update(params=params)

    def __str__(self):
        """Wrapper around request, returning a string instead of a dict"""
        return json.dumps(_sort_request(self))


class Request(Notification):
    #pylint:disable=line-too-long
    """Create a JSON-RPC `request object
    <http://www.jsonrpc.org/specification#request_object>`_.

        >>> Request('cat', name='Mittens')
        {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}, 'id': 1}

    :param method: The ``method`` name.
    :param args: Positional arguments added to ``params``.
    :param kwargs: Keyword arguments added to ``params``. Use ``request_id=x``
        to force the ``id`` to use.
    :returns: The JSON-RPC request in dictionary form.
    """
    #pylint:enable=line-too-long

    id_iterator = None

    def __init__(self, method, *args, **kwargs):
        # If 'request_id' is passed, use the specified id
        if 'request_id' in kwargs:
            _id = kwargs.pop('request_id', None)
        else: # Get the next id from the iterator
            # Create the iterator if not yet created
            if Request.id_iterator is None:
                Request.id_iterator = ids.from_config(config.ids)
            _id = next(self.id_iterator)
        # We call super last, after popping the request_id
        super(Request, self).__init__(method, *args, **kwargs)
        self.update(id=_id)
