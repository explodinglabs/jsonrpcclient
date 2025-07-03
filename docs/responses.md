# Parsing responses

The library includes a `parse` function which turns a deserialized response
into a nice namedtuple.

```python
>>> parse({"jsonrpc": "2.0", "result": "pong", "id": 1})
Ok(result='pong', id=1)
>>> parse({"jsonrpc": "2.0", "error": {"code": 1, "message": "There was an error", "data": None}, "id": 1})
Error(code=1, message='There was an error', data=None, id=1)
```

If you have a string, use `parse_json`.

```python
>>> parse_json('{"jsonrpc": "2.0", "result": "pong", "id": 1}')
Ok(result='pong', id=1)
```

To use the result, in Python versions prior to 3.10:

```python
from jsonrpcclient import Error, Ok
parsed = parse(response)
if isinstance(parsed, Ok):
    print(parsed.result)
elif isinstance(parse, Error):
    logging.error(parsed.message)
```

In Python 3.10+, use pattern matching:

```python
match parse(response):
    case Ok(result, id):
        print(result)
    case Error(code, message, data, id):
        logging.error(message)
```
