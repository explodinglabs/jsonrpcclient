> :warning: This master branch is for the upcoming version 4, currently [in
> release
> candidate](https://github.com/explodinglabs/jsonrpcclient/discussions/176).
> Read about the [changes in version
> 4](https://composed.blog/jsonrpcclient-4-changes), or read the [full
> documentation for v4](https://www.jsonrpcclient.com/en/latest/). For the
> stable release, jump to the [3.x
> branch](https://github.com/explodinglabs/jsonrpcclient/tree/3.x) or read the
> [full documentation for v3](https://www.jsonrpcserver.com/en/3.5.6/). Also,
> please pin your dependency to "jsonrpcclient<4" until you're ready to upgrade
> to v4.

<img
    alt="jsonrpcclient"
    style="margin: 0 auto;"
    src="https://github.com/explodinglabs/jsonrpcclient/blob/master/docs/logo.png?raw=true"
/>

Generate JSON-RPC requests and parse responses.

![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Downloads](https://pepy.tech/badge/jsonrpcclient/week)
![Checks](https://github.com/explodinglabs/jsonrpcclient/actions/workflows/checks.yml/badge.svg)
![Coverage Status](https://coveralls.io/repos/github/explodinglabs/jsonrpcclient/badge.svg?branch=master)

```sh
pip install --pre jsonrpcclient
```

```python
>>> from jsonrpcclient import parse, request
>>> import requests
>>> response = requests.post("http://localhost:5000/", json=request("ping"))
>>> parse(response.json())
Ok(result='pong', id=1)
```

Full documentation is at [jsonrpcclient.com](https://www.jsonrpcclient.com/en/latest/).

See also: [jsonrpcserver](https://github.com/explodinglabs/jsonrpcserver)
