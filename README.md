> September 1, 2021: Version 4 has been released. Read about the [changes in
> version 4](https://composed.blog/jsonrpcclient-4-changes). 

<img
    alt="jsonrpcclient"
    style="margin: 0 auto;"
    src="https://github.com/explodinglabs/jsonrpcclient/blob/main/docs/logo.png?raw=true"
/>

Generate JSON-RPC requests and parse responses in Python.

![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Code Quality](https://github.com/explodinglabs/jsonrpcclient/actions/workflows/code-quality.yml/badge.svg)
![Coverage Status](https://coveralls.io/repos/github/explodinglabs/jsonrpcclient/badge.svg?branch=main)
![Downloads](https://img.shields.io/pypi/dm/jsonrpcclient.svg)

```sh
pip install jsonrpcclient
```

```python
>>> from jsonrpcclient import parse, request
>>> import requests
>>> response = requests.post("http://localhost:5000/", json=request("ping"))
>>> parse(response.json())
Ok(result='pong', id=1)
```

Full documentation is at [jsonrpcclient.com](https://www.jsonrpcclient.com/).

See also: [jsonrpcserver](https://github.com/explodinglabs/jsonrpcserver)
