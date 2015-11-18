Send a request with ``send()``::

    >>> server.send({'jsonrpc': '2.0', 'method': 'cat', 'id': 1})

Sending a request is easier with ``request()``. It takes the ``method``,
followed by the arguments to the method::

    >>> server.request('cat', name='Mittens')

The return value is the *payload* (the ``result`` part of the JSON-RPC response
message).

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

Unlike single requests, batch requests return the whole JSON-RPC response
object, i.e. a list of responses for each request that had an ``id`` member.

.. note:: The server may not support batch requests.
