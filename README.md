<p align="center">
  <img alt="Logo" height="96" src="https://github.com/explodinglabs/jsonrpcclient/blob/main/docs/logo.png?raw=true" />
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/jsonrpcclient.svg" alt="PyPI" />
  <img src="https://github.com/explodinglabs/jsonrpcclient/actions/workflows/code-quality.yml/badge.svg" alt="Code Quality" />
  <img src="https://coveralls.io/repos/github/explodinglabs/jsonrpcclient/badge.svg?branch=main" alt="Coverage Status" />
  <img src="https://img.shields.io/pypi/dw/jsonrpcclient" alt="Downloads" />
  <img src="https://img.shields.io/github/license/explodinglabs/jsonrpcclient" alt="License" />
</p>

<p align="center">
  <i>Create JSON-RPC requests and parse responses in Python</i>
</p>

## Installation

```sh
pip install jsonrpcclient
```

## Usage

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

Full documentation is at [jsonrpcclient.com](https://www.jsonrpcclient.com/).

## 🎥 Video

https://github.com/user-attachments/assets/a59d8547-40b4-4e2f-9d99-d879cff6dc4e

## 📖 See Also

- [jsonrpcserver](https://github.com/explodinglabs/jsonrpcserver) – Process incoming JSON-RPC requests in Python
