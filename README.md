![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Coverage Status](https://coveralls.io/repos/github/bcb/jsonrpcclient/badge.svg?branch=master)

# jsonrpcclient

*Version 3 coming soon, see
[changelog](https://github.com/bcb/jsonrpcclient/blob/master/CHANGELOG.md).
Below usage is for version 3.*

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

```sh
pip install "jsonrpcclient[requests]"
```

```python
from jsonrpcclient.clients import http_client
http_client.request("http://cats.com", "speak")
```

Full documentation is at [jsonrpcclient.readthedocs.io](https://jsonrpcclient.readthedocs.io/).

## Testing

```sh
pip install "jsonrpcclient[unittest]"
pytest
```

See also: [jsonrpcserver](https://github.com/bcb/jsonrpcserver)
