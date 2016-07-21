Send a request::

    >>> response = server.request('cat', name='Mittens')
    --> {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 1}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}

The first argument is the JSON-RPC ``method``, followed by arguments to the
method.

The return value is the payload, (the ``result`` part of the response
message)::

    >>> response
    'meow'

If you're not interested in a response, use ``notify()`` instead of
``request()``.

Lower-Level
-----------

Send your own message with ``send()``::

    >>> server.send({'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}, 'id': 5})

A :class:`~request.Request` class is provided to simplify making a JSON-RPC
message::

    >>> Request('cat', name='Mittens', request_id=5)
    {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 5}

Send a :class:`~request.Request`::

    >>> server.send(Request('cat', name='Mittens', request_id=5))
    --> {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 5}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 5}
    'meow'

There's also a :class:`~request.Notification` class if you don't need a response.

Batch requests
--------------

With batch requests you can send multiple requests in a single message::

    >>> server.send([{'jsonrpc': '2.0', 'method': 'cat'}, {'jsonrpc': '2.0', 'method': 'dog'}])

Send multiple :class:`~request.Request` objects::

    >>> server.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    >>> server.send([Request('cube', i) for i in range(10)])

Unlike single requests, batch requests return the whole JSON-RPC response
object, i.e. a list of responses for each request that had an ``id`` member.

*The server may not support batch requests.*
