"""rpc.py"""

import itertools
from collections import OrderedDict

id_generator = itertools.count(1) # First generated is 1


def request(method, *args, **kwargs):
    """Returns an rpc notification, (a request not expecting a response.

    Notification examples:
        rpc.notification('go')
        rpc.notification('print', 'Hello world')
        rpc.notification('print', str='Hello world')

    Request examples (requiring a response):
        rpc.request('get', response=True)
        rpc.request('sqrt', 1, response=True)
        rpc.request('add', 1, 2, response=True)
        rpc.request('find', name='Beau', response=True)
        rpc.request('find', name='Beau', age=38, response=True)
    """

    # Get the request id
    request_id = None
    if kwargs.get('response', False):
        request_id = next(id_generator)

    # If 'response' is present in kwargs, pop it out of the dict
    if 'response' in kwargs:
        kwargs.pop('response')

    r = OrderedDict([
        ('jsonrpc', '2.0'),
        ('method', method)
    ])

    # Any params passed?
    if args or kwargs:

        params = None

        # Add any params passed as args
        if args:
            params = list(args)

        # Add any params passed as kwargs
        if kwargs:
            if params:
                params.append(OrderedDict(sorted(kwargs.items())))
            else:
                params = OrderedDict(sorted(kwargs.items()))

        r.update(OrderedDict([
            ('params', params)
        ]))

    # Add id if response=True was passed
    if request_id:
        r.update(OrderedDict([
            ('id', request_id)
        ]))

    return r
