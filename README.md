jsonrpcclient
=============

A JSON-RPC 2.0 client library for Python.

    >> import jsonrpcclient
    >> proxy = jsonrpcclient.Proxy('http://jsonrpcserver/')
    >> proxy.add(2, 3, response=True)
    5

Without *response=True* it's just a *notification*, which means you're not
expecting a response unless there's an error.

You can also use keyword arguments:

    >> proxy.find(42, foo='Bar')

That will send:

    {"jsonrpc": "2.0", "method": "find", "params": [42, {"foo": "bar"}]}

You will want to catch *RPCClientException* and handle it.

    try:
        proxy.go()

    except jsonrpcclient.exceptions.RPCClientException as e:
        print(str(e))
