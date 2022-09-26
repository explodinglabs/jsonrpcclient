<img
    alt="jsonrpcclient"
    style="margin: 0 auto;"
    src="https://github.com/explodinglabs/jsonrpcclient/blob/main/docs/logo.png?raw=true"
/>

![PyPI](https://img.shields.io/pypi/v/jsonrpcclient.svg)
![Code Quality](https://github.com/explodinglabs/jsonrpcclient/actions/workflows/code-quality.yml/badge.svg)
![Coverage Status](https://coveralls.io/repos/github/explodinglabs/jsonrpcclient/badge.svg?branch=main)
![Downloads](https://img.shields.io/pypi/dw/jsonrpcclient)

Generate JSON-RPC requests and parse responses in Python.

```sh
pip install jsonrpcclient
```

Generate a request:

```python
from jsonrpcclient import request, parse
req = request("ping")
# => {'jsonrpc': '2.0', 'method': 'ping', 'id': 1}
```

Parse a response:

```python
parsed = parse({"jsonrpc": "2.0", "result": "pong", "id": 1})
# => Ok(result='pong', id=1)
```
For strings, use `request_json` and `parse_json`. 

[Watch a video on how to use it](https://www.youtube.com/watch?v=PxQagaZ0PsY)

Full documentation is at [jsonrpcclient.com](https://www.jsonrpcclient.com/).

See also: [jsonrpcserver](https://github.com/explodinglabs/jsonrpcserver)
