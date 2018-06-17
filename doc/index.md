# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

```sh
$ pip install "jsonrpcclient[requests]"
```

```python
>>> import jsonrpcclient
>>> jsonrpcclient.request('http://cats.com', 'speak')
--> {"jsonrpc": "2.0", "method": "speak", "id": 1}
<-- {"jsonrpc": "2.0", "result": "meow", "id": 1} (200 OK)
'meow'
```

This example uses the *requests* library for sending, but more options are
available. See [examples in various frameworks](examples.html), or read the
[guide to usage and configuration](api.html).

Contribute on [Github](https://github.com/bcb/jsonrpcclient).

See also: [jsonrpcserver](https://jsonrpcserver.readthedocs.io/)
