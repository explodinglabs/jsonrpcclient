.. _Request: api.html#request

Send a request with ``send()``::

    >>> server.send({'jsonrpc': '2.0', 'method': 'cat', 'id': 1})
    --> {'jsonrpc': '2.0', 'method': 'cat', 'id': 1}

Sending a request is easier with ``request()``. It takes the ``method``, followed
by the ``params``::

    >>> server.request('cat', name='Mittens')
    --> {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}, 'id': 1}

If you're not interested in a response, use ``notify()`` instead of
``request()``.

..
    >>> server.notify('cat', name='Mittens')
    --> {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}}

``request()`` and ``notify()`` are wrappers around ``send(Request())`` and
``send(Notification())``. The `API <Request_>`_ has more informat about making
requests.

Batch requests
--------------

Batch requests send many requests in one message::

    >>> server.send([{'jsonrpc': '2.0', 'method': 'cat'}, {'jsonrpc': '2.0', 'method': 'dog'}])

Send multiple `Request`_ objects::

    >>> server.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    >>> server.send([Request('cube', i) for i in range(10)])

.. note:: The server may not support batch requests.
