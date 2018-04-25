![Coverage Status](https://coveralls.io/repos/github/bcb/jsonrpcclient/badge.svg?branch=master)

# jsonrpcclient

[![Join the chat at https://gitter.im/bcb/jsonrpcclient](https://badges.gitter.im/bcb/jsonrpcclient.svg)](https://gitter.im/bcb/jsonrpcclient?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python 2.7 and 3.3+.

```sh
$ pip install 'jsonrpcclient[requests]'
```
```python
import jsonrpcclient
jsonrpcclient.request('http://cats.com', 'speak')
```

Full documentation is at [jsonrpcclient.readthedocs.io](https://jsonrpcclient.readthedocs.io/).

See also: [jsonrpcserver](https://github.com/bcb/jsonrpcserver)
