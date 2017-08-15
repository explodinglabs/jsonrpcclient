# jsonrpcclient

Send [JSON-RPC](http://www.jsonrpc.org/) requests in Python 2.7 and 3.3+.

```sh
pip install jsonrpcclient[requests]
```
```python
import jsonrpcclient
jsonrpcclient.request('http://cats.com', 'speak')
```
```sh
--> {"jsonrpc": "2.0", "method": "speak", "id": 1}
<-- {"jsonrpc": "2.0", "result": "meow", "id": 1} (200 OK)
'meow'
```

Full documentation is at [jsonrpcclient.readthedocs.io](https://jsonrpcclient.readthedocs.io/).

See also: [jsonrpcserver](https://github.com/bcb/jsonrpcserver)
