# Generating requests

## The request function

Generate a request with the `request` function:

```python
>>> from jsonrpcclient import request, request_json
>>> request("ping")
{'jsonrpc': '2.0', 'method': 'ping', 'id': 1}
```

`request_json` gives a string:

```py
>>> request_json("ping")
'{"jsonrpc": "2.0", "method": "ping", "id": 2}'
```

It simply applies `str` after `request`.

## Ids

Subsequent calls increment the `id`:

```

> > > request("ping")
> > > {"jsonrpc": "2.0", "method": "ping", "2.0", "id": 3}
> > > request("ping")
> > > {"jsonrpc": "2.0", "method": "ping", "2.0", "id": 4}

```

Use an explicit `id`:

```

> > > request("ping", id="foo")
> > > {"jsonrpc": "2.0", "method": "ping", "2.0", "id": "foo"}

```

Or generate a different type of `id`:

```python
>>> from jsonrpcclient import request_hex, request_random, request_uuid
>>> request_hex("foo")
{"jsonrpc": "2.0", "method": "foo", "id": "1"}
>>> request_random("foo")
{"jsonrpc": "2.0", "method": "foo", "id": "qzsib147"}
>>> request_uuid("foo")
{"jsonrpc": "2.0", "method": "foo", "id": "45480a2f-069c-42aa-a67f-f6fdd83d6026"}
```

## Parameters

Pass `params` to include parameters in the payload. This should be either a
tuple for positional arguments, or dict for keyword arguments.

```python
>>> request("ping", params=(1,))
{"jsonrpc": "2.0", "method": "ping", "2.0", "params": [1], "id": 5}
>>> request("ping", params={"key": "val"})
{"jsonrpc": "2.0", "method": "ping", "2.0", "params": {"key": "val"}, "id": 6}
```

## JSON requests

If you need the request serialized to a string, use `request_json`:

```python
>>> from jsonrpcclient import request_json
>>> request_json("foo")
'{"jsonrpc": "2.0", "method": "foo", "id": 6}'
```

You can also use request_json_hex etc., for the other id types.

## Batch requests

```python
>>> import json
>>> json.dumps([request("foo") for _ in range(3)])
'[{"jsonrpc": "2.0", "method": "foo", "id": 7}, {"jsonrpc": "2.0", "method": "foo", "id": 8}, {"jsonrpc": "2.0", "method": "foo", "id": 9}]'
```

## Notifications

Use the `notification` function instead of `request`:

```python
>>> from jsonrpcclient import notification
>>> notification("ping")
{"jsonrpc": "2.0", "method": "ping"}
```

As with `request_json`, `notification_json` will give you the notification as a
JSON string.

```python
>>> from jsonrpcclient import notification_json
>>> notification_json("ping")
'{"jsonrpc": "2.0", "method": "ping"}'
```
