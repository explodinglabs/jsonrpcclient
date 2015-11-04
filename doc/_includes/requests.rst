Send a request::

    >>> server.send({'jsonrpc': '2.0', 'method': 'cat'})

Send a list of requests (if the server supports batch calls)::

    >>> server.send([{'jsonrpc': '2.0', 'method': 'cat'}, {'jsonrpc': '2.0', 'method': 'dog'}])

The Request class
-----------------

The Request class makes it easier to make JSON-RPC requests::

    >>> from jsonrpcclient import Request
    >>> Request('cat')
    {'jsonrpc': '2.0', 'method': 'cat'}

The first argument to ``Request()`` is the *method*; everything else is
*arguments* to the method::

    >>> Request('multiply', 5, 3)
    {'jsonrpc': '2.0', 'method': 'multiply', params: [5, 3]}

Keyword arguments are also acceptable::

    >>> Request('cat', action='speak')
    {'jsonrpc': '2.0', 'method': 'cat', 'params': {'action': 'speak'}}

To get response back, specify a request id::

    >>> Request('cat', request_id=1)
    {'jsonrpc': '2.0', 'method': 'cat', id=1}

Or use an auto-iterated id::

    >>> Request('cat', response=True)
    {'jsonrpc': '2.0', 'method': 'cat', id=1}
    >>> Request('cat', response=True)
    {'jsonrpc': '2.0', 'method': 'cat', id=2}

If you prefer, call the method directly on the ``Request`` class::

    >>> Request.cat()
    {'jsonrpc': '2.0', 'method': 'cat'}
    >>> Request.multiply(5, 3, response=True)
    {'jsonrpc': '2.0', 'method': 'multiply', params: [5, 3], id=3}

Back to sending requests...
---------------------------

Send a request using the ``Request`` class::

    >>> server.send(Request('cat'))

Send a list of requests::

    >>> server.send([Request('cat'), Request('dog')])

Send a request using a shorthand version::

    >>> server.request('cat') # short for server.send(Request('cat'))

Shorter still, is to call the method directly on the ``Server`` object::

    >>> server.cat() # short for server.send(Request('cat'))

.. note:: ``notify()`` is deprecated. Use ``request()`` instead.
