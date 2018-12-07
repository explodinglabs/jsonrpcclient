# Jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Downloads](https://pepy.tech/badge/jsonrpcclient)
![Coverage Status](https://coveralls.io/repos/github/bcb/jsonrpcclient/badge.svg?branch=master)

*Version 3 is out. It's Python 3.5+ only. See the
[changelog](https://github.com/bcb/jsonrpcclient/blob/master/CHANGELOG.md),
[example usage](https://jsonrpcclient.readthedocs.io/en/latest/examples.html),
and read the [updated documentation](https://jsonrpcclient.readthedocs.io/).*

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

## Testing

```sh
pip install "jsonrpcclient[unittest]" mypy
pytest
mypy jsonrpcclient
```

See also: [jsonrpcserver](https://github.com/bcb/jsonrpcserver)
