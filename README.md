jsonrpcclient
=============

A JSON-RPC 2.0 client library for Python.

    >> import jsonrpcclient
    >> proxy = jsonrpcclient.Proxy('http://jsonrpcserver/')
    >> proxy.add(2, 3, response=True)
    5

Without ``response=True``, your message is just a notification, which means
you're not expecting a response.

You can also use keyword arguments like any other python function:

    >> result = proxy.get(42, name='Foo', response=True)
    --> {"jsonrpc": "2.0", "method": "find", "params": [42, {"name": "Foo"}]}

Set your log level to INFO (or higher) to see the messages being sent and
received.

You will want to catch *RPCClientException* and handle it.

    try:
        proxy.go()

    except jsonrpcclient.exceptions.RPCClientException as e:
        print(str(e))
