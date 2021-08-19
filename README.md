> :warning: This master branch is for the upcoming version 4,
> currently [in development](https://github.com/explodinglabs/jsonrpcclient/discussions/176) (read: [The future of this
> library](https://github.com/explodinglabs/jsonrpcclient/discussions/171)).
> For the latest stable release, see the [3.x
> branch](https://github.com/explodinglabs/jsonrpcclient/tree/3.x). Also,
> please pin your dependency to "jsonrpcclient<4" until you're ready to upgrade
> to v4.

# jsonrpcclient

Generate JSON-RPC requests and parse responses.

![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Downloads](https://pepy.tech/badge/jsonrpcclient/week)
![Coverage Status](https://coveralls.io/repos/github/explodinglabs/jsonrpcclient/badge.svg?branch=master)

```sh
pip install --pre jsonrpcclient
```

```python
>>> from jsonrpcclient import request
>>> request("get")
'{"jsonrpc": "2.0", "method": "get", "id": 1}'
```

Full documentation is at [jsonrpcclient.com](https://www.jsonrpcclient.com/en/latest/).

See also: [jsonrpcserver](https://www.jsonrpcserver.com/)
