jsonrpcclient
=============

A [JSON-RPC 2.0](http://www.jsonrpc.org/) client library for Python 3.

    >> import jsonrpcclient
    >> proxy = jsonrpcclient.Proxy('http://jsonrpcserver/')
    >> proxy.add(2, 3, response=True)
    5

The library converts the ``add()`` call into a JSON-RPC message, which is sent
to the server.

Set your logging level to ``INFO`` to see the messages being sent and received.

    >> logging.basicConfig(level=logging.INFO)
    >> proxy.add(2, 3, response=True)
    --> {"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 5, "id": 1}
    5

``response=True`` tells the server you're expecting a response.

You can pass any number of positional or keyword arguments, and they will be
translated into JSON-RPC.

    >> result = proxy.find(42, name='Foo', response=True)
    --> {"jsonrpc": "2.0", "method": "find", "params": [42, {"name": "Foo"}], "id": 1}
    <-- {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

You should catch ``RPCClientException``, in case there's a connection problem,
or your request was unsuccessful.

    try:
        proxy.go()

    except jsonrpcclient.exceptions.RPCClientException as e:
        print(str(e))

If you need a server, try my
[jsonrpcserver](https://bitbucket.org/beau-barker/jsonrpcserver) library.
