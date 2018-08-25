![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Coverage Status](https://coveralls.io/repos/github/bcb/jsonrpcclient/badge.svg?branch=master)

# jsonrpcclient

*Version 3 is out. See the
[changelog](https://github.com/bcb/jsonrpcclient/blob/master/CHANGELOG.md) and
[read the docs](https://jsonrpcclient.readthedocs.io/).*

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

```sh
pip install "jsonrpcclient[requests]"
```

```python
from jsonrpcclient.clients.http_client import HTTPClient
client = HTTPClient("http://localhost:5000")
response = client.request("ping")
>>> response.text
'{"jsonrpc": "2.0", "result": "pong", "id": 1}'
>>> response.data.ok
True
>>> response.data.result
'pong'
```

Full documentation is at [jsonrpcclient.readthedocs.io](https://jsonrpcclient.readthedocs.io/).

## Testing

```sh
pip install "jsonrpcclient[unittest]"
pytest
pip install mypy
mypy jsonrpcclient
```

See also: [jsonrpcserver](https://github.com/bcb/jsonrpcserver)
