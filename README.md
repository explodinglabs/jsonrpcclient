# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python 2.7 and 3.3+.

```python
from jsonrpcclient.http_client import HTTPClient
HTTPClient('http://cats.com/').request('speak')
```
```sh
--> {"jsonrpc": "2.0", "method": "speak", "id": 1}
<-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
'meow'
```

Full documentation is at [jsonrpcclient.readthedocs.io](https://jsonrpcclient.readthedocs.io/).

See also: [jsonrpcserver](https://github.com/bcb/jsonrpcserver)
