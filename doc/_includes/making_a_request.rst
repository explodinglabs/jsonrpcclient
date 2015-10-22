Make a request::

    >>> server.request('cube', 3)
    27

The first argument to ``request()`` is the *method*; everything else is
*arguments* to the method. Keyword arguments are also acceptable::

    >>> server.request('find', name='Foo', age=42)
    --> {"jsonrpc": "2.0", "method": "find", "params": {"name": "Foo", "age": 42}, "id": 1}
    <-- {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

.. tip::

    To see the underlying JSON-RPC messages going back and forth, see the
    Logging_ section below.

If you don't need any data returned, use ``notify()`` instead of
``request()``::

    server.notify('go')
