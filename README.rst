=============
jsonrpcclient
=============

A `JSON-RPC 2.0 <http://www.jsonrpc.org/>`_ client library for Python 3.

Define the server, then use ``request()`` to make a remote procedure call.

.. sourcecode:: python

    >>> import jsonrpcclient
    >>> server = jsonrpcclient.Server('http://endpoint')
    >>> server.request('add', 2, 3)
    --> {"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 5, "id": 1}
    5

If you don't need any data to be returned, use ``notify()`` instead:

.. sourcecode:: python

    >>> server.notify('go')
    --> {"jsonrpc": "2.0", "method": "go"}
    >>>

You can pass any number of positional or keyword arguments, and they will be
translated into JSON-RPC.

.. sourcecode:: python

    >>> result = server.request('find', 42, name='Foo')
    --> {"jsonrpc": "2.0", "method": "find", "params": [42, {"name": "Foo"}], "id": 1}
    <-- {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

You should catch ``RPCClientException``. This will be raised in the event of
errors such as connection problems, or if the server responded with JSON-RPC
*error* response.

.. sourcecode:: python

    try:
        server.go()
    except jsonrpcclient.exceptions.RPCClientException as e:
        print(str(e))

Shorthand
---------

There's another way to send messages:

.. sourcecode:: python

    >>> server.add(2, 3, response=True)
    --> {"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 5, "id": 1}
    5

The library catches the undefined ``add()`` call, and sends it as a JSON-RPC
message.

``response=True`` tells the server you're expecting a response, without that
it's a notification.

Logging
-------

If you don't want the log entries, turn them off with:

.. sourcecode:: python

    logging.getLogger('jsonrpcclient').setLevel(logging.INFO)

If you need a server, try my `jsonrpcserver
<https://bitbucket.org/beau-barker/jsonrpcserver>`_ library.
