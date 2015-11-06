.. _Request: api.html#request

Send a request with ``send()``::

    >>> server.send({'jsonrpc': '2.0', 'method': 'cat', 'id': 1})
    --> {'jsonrpc': '2.0', 'method': 'cat', 'id': 1}

Send a request with ``request()``::

    >>> server.request('cat', name='Mittens')
    --> {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}, 'id': 1}

The return value is *payload* (the ``result`` part of the JSON-RPC response).

If you're not interested in a response, use ``notify()`` instead of ``request()``.

..
    >>> server.notify('cat', name='Mittens')
    --> {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}}

``request()`` and ``notify()`` are wrappers around ``send(Request())`` and
``send(Notification())``. Read the `API <Request_>`_ to learn more about making
requests.

Batch requests
--------------

Batch requests let you send many requests in one single message::

    >>> server.send([{'jsonrpc': '2.0', 'method': 'cat'}, {'jsonrpc': '2.0', 'method': 'dog'}])

Send multiple `Request`_ objects::

    >>> server.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    >>> server.send([Request('cube', i) for i in range(10)])

Unlike a single request, batch requests return the full JSON-RPC response, i.e.
a ``list`` containing one response object for every request (excluding
notifications).

.. note:: The server may not support batch requests.
