# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

```sh
$ pip install "jsonrpcclient[requests]"
```

```python
>>> from jsonrpcclient.clients.http_client import HTTPClient
>>> client = HTTPClient("http://localhost:5000")
>>> response = client.request("ping").data.result
'pong'
```

This example uses the *requests* library for sending, but more options are
available. See [examples in various frameworks](examples.html), or read the
[guide to usage and configuration](api.html).

Contribute on [Github](https://github.com/bcb/jsonrpcclient).

See also: [jsonrpcserver](https://jsonrpcserver.readthedocs.io/)
