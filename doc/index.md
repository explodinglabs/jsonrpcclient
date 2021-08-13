# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

```sh
$ pip install "jsonrpcclient[requests]"
```

```python
>>> from jsonrpcclient import request
>>> response = request("http://fruits.com", "get", color="yellow")
>>> response.text
'{"jsonrpc": "2.0", "result": ["banana", "lemon", "mango"], "id": 1}'
>>> response.data.result
['banana', 'lemon', 'mango']
```

This example uses the *requests* library for sending, but more options are
available. See [examples in various frameworks](examples.html), or read the
[guide to usage and configuration](api.html).

Contribute on [Github](https://github.com/explodinglabs/jsonrpcclient).

See also: [jsonrpcserver](https://jsonrpcserver.readthedocs.io/)
