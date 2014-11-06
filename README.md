jsonrpcclient
=============

A [JSON-RPC 2.0](http://www.jsonrpc.org/) client library for Python 3.

    >> import jsonrpcclient
    >> proxy = jsonrpcclient.Proxy('http://jsonrpcserver/')
    >> proxy.request('add', 2, 3)
    5

The shorthand version uses Python magic:

    >> proxy.add(2, 3)
    --> {"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 5, "id": 1}
    5

Set your logging level to ``INFO`` to see the messages being sent and received.

You can also pass keyword arguments, and they'll be translated into JSON-RPC.

    >> result = proxy.find(42, name='Foo')
    --> {"jsonrpc": "2.0", "method": "find", "params": [42, {"name": "Foo"}], "id": 1}
    <-- {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

To send a *notification*, use ``notify()``. This tells the server you're not
expecting any response.

    >> proxy.notify('store', firstname='Foo', lastname='Bar')
    --> {"jsonrpc": "2.0", "method": "beep", "params": {"firstname": "Foo", "last": "Bar"]}

You will want to catch ``RPCClientException`` in case there's a connection
problem, or your request was unsuccessful.

    try:
        proxy.go()
    except jsonrpcclient.exceptions.RPCClientException as e:
        print(str(e))

If you need a server library, try my
[jsonrpcserver](https://bitbucket.org/beau-barker/jsonrpcserver).
