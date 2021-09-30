# FAQ

## How to use a different json library?

The `request_json` function is simply `json.dumps` after `request`, and the
`parse_json` function is simply `parse` after `json.loads`.

So here's how one could write their own, using a different json library (ujson
here):

```python
from jsonrpcclient import request, parse
from jsonrpcclient.utils import compose
import ujson

parse_json = compose(parse, ujson.loads)
request_json = compose(ujson.dumps, request)
```
