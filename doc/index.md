# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

```sh
$ pip install "jsonrpcclient[requests]"
```

```python
import jsonrpcclient
response = jsonrpcclient.request("http://localhost:5000", "ping")
>>> response.text
'{"jsonrpc": "2.0", "result": "pong", "id": 1}'
>>> response.data.result
'pong'
```

This example uses the *requests* library for sending, but more options are
available. See [examples in various frameworks](examples.html), or read the
[guide to usage and configuration](api.html).

Contribute on [Github](https://github.com/bcb/jsonrpcclient).

See also: [jsonrpcserver](https://jsonrpcserver.readthedocs.io/)
