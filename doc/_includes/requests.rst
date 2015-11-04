Send a request::

    >>> server.send({'jsonrpc': '2.0', 'method': 'cat', 'id': 1})

Send a batch of requests in one go::

    >>> server.send([
            {'jsonrpc': '2.0', 'method': 'cat'},
            {'jsonrpc': '2.0', 'method': 'dog'}])

The Request class
-----------------

The Request class makes it easy to build JSON-RPC requests::

    >>> from jsonrpcclient import Request
    >>> Request('cat')
    {'jsonrpc': '2.0', 'method': 'cat'}

The first argument to ``Request()`` is the *method*; everything else is
*arguments* to the method::

    >>> Request('multiply', 5, 3)
    {'jsonrpc': '2.0', 'method': 'multiply', params: [5, 3]}

Keyword arguments are also acceptable::

    >>> Request('cat', action='speak')
    {"jsonrpc": "2.0", "method": "cat", "params": {"action": "speak"}}

In JSON-RPC, to get response back we must specify an ``id`` for the request::

    >>> Request('cat', request_id=1)
    {"jsonrpc": "2.0", "method": "cat", id=1}

To use an auto-iterated id, use ``response=True``::

    >>> Request('cat', response=True)
    {"jsonrpc": "2.0", "method": "cat", id=1}
    >>> Request('cat', response=True)
    {"jsonrpc": "2.0", "method": "cat", id=2}

If you prefer, an alternative way is to call the method name directly::

    >>> Request.cat()
    {"jsonrpc": "2.0", "method": "cat"}
    >>> Request.multiply(5, 3, request_id=1)
    {"jsonrpc": "2.0", "method": "multiply", params: [5, 3], id=1}

Back to sending requests
------------------------

Send a Request::

    >>> server.send(Request('cat'))

Send a batch of Requests::

    >>> server.send([Request('cat'), Request('dog')])

Shorthand for sending a single request::

    >> server.request('cat')

Even shorter, call the method name directly::

    >> server.cat()
