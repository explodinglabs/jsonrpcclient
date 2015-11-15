Send a request with ``send()``::

    >>> server.send({'jsonrpc': '2.0', 'method': 'cat', 'id': 1})

Sending a request is easier with :meth:`server.Server.request`. It takes the
``method``, followed by the ``params``::

    >>> server.request('cat', name='Mittens')

If you're not interested in a response, use ``notify()`` instead of
``request()``.

Batch requests
--------------

Send multiple requests in one message::

    >>> server.send([{'jsonrpc': '2.0', 'method': 'cat'}, {'jsonrpc': '2.0', 'method': 'dog'}])

Send multiple :class:`Request <request.Request>` objects::

    >>> server.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    >>> server.send([Request('cube', i) for i in range(10)])

.. note:: The server may not support batch requests.
