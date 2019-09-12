# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Downloads](https://pepy.tech/badge/jsonrpcclient)
![Coverage Status](https://coveralls.io/repos/github/bcb/jsonrpcclient/badge.svg?branch=master)

```sh
pip install "jsonrpcclient[requests]"
```

```python
>>> from jsonrpcclient import request
>>> response = request("http://fruits.com", "get", color="yellow")
>>> response.text
'{"jsonrpc": "2.0", "result": ["banana", "lemon", "mango"], "id": 1}'
>>> response.data.result
['banana', 'lemon', 'mango']
```

Full documentation is at [jsonrpcclient.readthedocs.io](https://jsonrpcclient.readthedocs.io/).

See also: [jsonrpcserver](https://github.com/bcb/jsonrpcserver)
