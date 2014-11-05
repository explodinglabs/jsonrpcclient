jsonrpcclient
=============

A JSON-RPC 2.0 client library for Python.

    >> import jsonrpcclient
    >> proxy = jsonrpcclient.Proxy('http://jsonrpcserver/')
    >> proxy.add(2, 3, response=True)
    5

Without ``response=True``, your message is just a notification, which means
you're not expecting a response.

You can also pass keyword arguments like any other python function, and they'll
be translated into JSON-RPC.

    >> result = proxy.get(42, name='Foo', response=True)
    --> {"jsonrpc": "2.0", "method": "find", "params": [42, {"name": "Foo"}], "id": 1}

Set your logging level to ``INFO`` or higher to see the messages being sent and
received.

You will want to catch ``RPCClientException`` in case there's a connection
problem or your request was unsuccessful and the server responded with "error".

    try:
        proxy.go()

    except jsonrpcclient.exceptions.RPCClientException as e:
        print(str(e))
