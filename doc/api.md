<p class="rubric"><a class="reference internal" href="index.html"><span class="doc">jsonrpcclient</span></a></p>

# jsonrpcclient Guide

This library allows you to call remote procedures.

## Installation

Install the package with the *Requests* library (alternatively, see [other
options](examples.html)):

```sh
$ pip install "jsonrpcclient[requests]"
```

For Python versions 2.7-3.4, install a 2.x version.

```sh
$ pip install "jsonrpcclient[requests]"==2.* # 2.\* works in my shell
```

## Sending a request

If using HTTP, the easiest way to send a request is using the convenience
methods:

```python
>>> from jsonrpcclient.clients import http_client
>>> http_client.request("http://cats.com", "speak")
'meow'
```

The first argument is the endpoint, and the second argument is the method to
call. Subsequent arguments are arguments to the method.

Use `notify` instead of `request` to signify that no response is required:

```python
>>> http_client.notify('http://cats.com', 'speak')
--> {"jsonrpc": "2.0", "method": "speak"}
<--
>>>
```

Alternatively, instantiate `HTTPClient`, passing the server endpoint:

```python
>>> from jsonrpcclient.clients.http_client import HTTPClient
>>> client = HTTPClient('http://pets.com')
```

Then we can send multiple requests with the `client` object.

### Send

Send a request, passing the whole JSON-RPC request object:

```python
>>> client.send('{"jsonrpc": "2.0", "method": "ping", "id": 1}')
--> {"jsonrpc": "2.0", "method": "ping", "id": 1}
<-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
'pong'
```

### Request

Send a request by passing the method and arguments. This is the main public
method.

```python
>>> client.request('cat', name='Mittens')
--> {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 1}
<-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
'meow'
```

If you're not interested in a response, use `notify()` instead of `request()`.

### The Request class

This class makes it easy to create a JSON-RPC [request
object](http://www.jsonrpc.org/specification#request_object):

```python
>>> from jsonrpcclient.request import Request
>>> Request('cat', name='Mittens')
{'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}, 'id': 1}
```

Send a `Request` object:

```python
>>> client.send(Request('ping'))
--> {"jsonrpc": "2.0", "method": "ping", "id": 1}
<-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
'pong'
```

The `request` method above is a wrapper around `send(Request())`.

If you're not interested in a response, use the `Notification` class instead of
`Request`.

### Batch requests

JSON-RPC allows you to send multiple requests in a single message:

```python
req = '''[
    {"jsonrpc": "2.0", "method": "cat", "id": 1},
    {"jsonrpc": "2.0", "method": "dog", "id": 2}
]'''
client.send(req)
```

Send multiple `Request` objects:

```python
client.send([Request('cat'), Request('dog')])
```

Using list comprehension to get the cube of ten numbers:

```python
client.send([Request('cube', i) for i in range(10)])
```

Unlike single requests, batch requests return the whole JSON-RPC [batch
response](http://www.jsonrpc.org/specification#batch) - a list of responses for
each request that had an `id` member.

*The server may not support batch requests.*

## Configuration

Most public methods can take the following optional parameters:

**id_generator**

Specifies a generator which will be used to create the "id" part of the
JSON-RPC request. Some built-in options are in the ids module: decimal,
hexadecimal, random and uuid. Default is *ids.decimal()*.

Example:
```python
>>> from jsonrpcclient import ids
>>> random_ids = ids.random()
>>> client.request("ping", id_generator=random_ids)
--> {"jsonrpc": "2.0", "method": "ping", "id": "9zo2a2xb"}
```

**request_id**

Specifies the "id" part of the JSON-RPC request. Default is *None*, which calls
`next()` on the last id generator that was used.

Example:
```python
>>> request("http://localhost:5000", "ping", request_id="foo")
--> {"jsonrpc": "2.0", "method": "ping", "id": "foo"}
```

**trim_log_values**

Show abbreviated requests and responses in logs. Default is *False*.

**validate_against_schema**

Validate responses against the JSON-RPC schema. Default is *True*.

### Configuring the Requests library

HTTPClient makes use of Kenneth Reitz's Requests library. The [Session]
(http://docs.python-requests.org/en/master/api/#requests.Session) is available
so you can configure it before sending any requests.

For example, Basic Auth:

```python
client.session.auth = ('user', 'pass')
```

SSL authentication:

```python
client.session.verify = '/path/to/certificate'
```

Custom HTTP headers:

```python
client.session.headers.update({'Content-Type': 'application/json-rpc'})
```

You can also configure some Requests options when calling `send`:

```python
client.send(req, verify=True, cert='/path/to/certificate',
            headers={'Content-Type': 'application/json-rpc'})
```

As in the Requests library, any dictionaries passed to `send` in named
arguments will be merged with the session-level values that are set. The
method-level parameters override session parameters.

## Disable logging

To disable logging:

```python
import logging
logging.getLogger("jsonrpcclient.client.request").setLevel(logging.WARNING)
logging.getLogger("jsonrpcclient.client.response").setLevel(logging.WARNING)
```
