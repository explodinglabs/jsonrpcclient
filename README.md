> :warning: This master branch is for the upcoming version 4,
> currently in development (read: [The future of this
> library](https://github.com/explodinglabs/jsonrpcclient/discussions/171)).
> For the latest stable release, see the [3.x
> branch](https://github.com/explodinglabs/jsonrpcclient/tree/3.x). Also,
> please pin your dependency to "jsonrpcclient<4" until you're ready to upgrade
> to v4.

# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python.

![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Downloads](https://pepy.tech/badge/jsonrpcclient/week)
![Coverage Status](https://coveralls.io/repos/github/explodinglabs/jsonrpcclient/badge.svg?branch=master)

```sh
pip install --pre jsonrpcclient
```

```python
>>> import requests
>>> from jsonrpcclient import request, parse
>>> response = requests.post("https://random.org/", json=request("ping"))
>>> parsed = parse(response.json()
```

Full documentation is at [jsonrpcclient.com](https://www.jsonrpcclient.com/en/latest/).

See also: [jsonrpcserver](https://github.com/explodinglabs/jsonrpcserver)
