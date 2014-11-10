=============
jsonrpcclient
=============

A `JSON-RPC 2.0 <http://www.jsonrpc.org/>`_ client library for Python 3.

An example of adding two numbers:

.. sourcecode:: python

    >>> import jsonrpcclient
    >>> proxy = jsonrpcclient.Proxy('http://endpoint/')
    >>> proxy.add(2, 3, response=True)
    --> {"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 5, "id": 1}
    5

The library catches the unknown add call, and sends it as a JSON-RPC
message. response=True tells the server you're expecting a response.

You can pass any number of positional or keyword arguments, and they will be
translated into JSON-RPC.

.. sourcecode:: python

    >>> result = proxy.find(42, name='Foo', response=True)
    --> {"jsonrpc": "2.0", "method": "find", "params": [42, {"name": "Foo"}], "id": 1}
    <-- {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

