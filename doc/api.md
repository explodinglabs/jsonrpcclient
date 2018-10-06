<p class="rubric"><a class="reference internal" href="index.html"><span class="doc">jsonrpcclient</span></a></p>

# jsonrpcclient Guide

This library allows you to call remote procedures using the JSON-RPC message
format.

## Installation

Install the package with the *Requests* library (alternatively, see [other
options](examples.html)):

```sh
$ pip install "jsonrpcclient[requests]"
```

For Python versions older than 3.5, install a 2.x version, and jump over to
[the 2.x docs](https://jsonrpcclient.readthedocs.io/en/2.6.0/).

```sh
$ pip install "jsonrpcclient[requests]>2,<3"
```

## Usage

The simplest way to send a standard http request is to use the convenience
function `request`.

```python
from jsonrpcclient import request
response = request("http://cats.com", "speak", name="Yoko")
```

The arguments to `request` are: the http server's endpoint url, the RPC method
to call, followed by any arguments to the method.

The `response.data.result` contains the payload back from the server.

```python
>>> print(response.data.result)
'meow'
```

For more advanced usage, read on.

Create a client object to work with:

```python
from jsonrpcclient.clients.http_client import HTTPClient
client = HTTPClient("http://cats.com")
```

Send a request:

```python
response = client.send('{"jsonrpc": "2.0", "method": "ping", "id": 1}')
```

Instead of typing the whole JSON-RPC request string, a `Request` class makes
it easy for you:

```python
>>> from jsonrpcclient.requests import Request
>>> Request("ping")
{'jsonrpc': '2.0', 'method': 'ping', 'id': 1}
```

The first argument to `Request` is the remote method to call, and subsequent
ones are arguments to the method.

```python
>>> Request("cat", name="Yoko")
{'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Yoko'}, 'id': 1}
```

Pass a `request_id` to specify the "id" part of the JSON-RPC request.

```python
>>> Request("ping", request_id="foo")
--> {"jsonrpc": "2.0", "method": "ping", "id": "foo"}
```

If a request id is not specified, one is generated for the request.

Sending a `Request` object:

```python
response = client.send(Request("ping"))
```

If a response is not required, use the `Notification` class instead of
`Request`.

A `request()` method is provided which wraps `send(Request())`.

```python
response = client.request("ping")
```

If a response is not required, use `notify` instead of `request`.

```python
client.notify("speak")
```

## Batch requests

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
responses = client.send([Request("cat"), Request("dog")])
```

The server may not support batch requests.

## Response

A Response object is returned from the `send`, `request` and `notify` methods.

The object has three attributes:

- `text`: This is the response text received from the server.
- `raw`: The framework's own response object, e.g. for the HTTP client this
    is the _requests_ library's Response object.
- `data`: The parsed response. (see below)

For single requests, `data` contains the following attributes:

- `id`: The request ID.
- `result`: The result part of the JSON-RPC response message. This is
  the payload you've requested from the server.

For batch requests, `data` is a list of responses. When iterating over the
responses, check the `ok` attribute.

```python
for responses in response.data:
    if response.ok:
        print(response.result)
    else:
        logging.error(response.message)
```

If `ok` is False, the other attributes are `message`, `code` and `data`.

If the request wasn't successful, an exception will be raised.

## Configuration

Any of the following options can be configured in:

- arguments to send/request/notify.
- arguments to the client;
- the config file (see below);

**basic_logging**

Adds log handlers, to log incoming/outgoing messages to stderr. (this option
can't be passed to send/request/notify, only to the client or config file.)

**id_generator**

Specifies a generator which will be used to create the "id" part of the
JSON-RPC request. Some built-in options are in the id_generators module:
decimal, hexadecimal, random and uuid. Default is *id_generators.decimal()*.

Example:
```python
>>> from jsonrpcclient import id_generators
>>> random_ids = id_generators.random()
>>> client.request("ping", id_generator=random_ids)
--> {"jsonrpc": "2.0", "method": "ping", "id": "9zo2a2xb"}
```

**trim_log_values**

Show abbreviated requests and responses in logs. Default is *False*.

**validate_against_schema**

Validate responses against the JSON-RPC schema. Default is *True*.

### Config file

Here's an example of the config file `.jsonrpcclientrc` - this should be
placed in the current or home directory:

```ini
[general]
basic_logging = no
id_generator = jsonrpcclient.id_generators.decimal
trim_log_values = no
validate_against_schema = yes
```

### Configuring the Requests library

HTTPClient makes use of Kenneth Reitz's Requests library. The
[Session](http://docs.python-requests.org/en/master/api/#requests.Session)
is available so you can configure it before sending any requests.

For example, Basic Auth:

```python
client.session.auth = ("user", "pass")
```

SSL authentication:

```python
client.session.verify = "/path/to/certificate"
```

Custom HTTP headers:

```python
client.session.headers.update({"Content-Type": "application/json-rpc"})
```

You can also configure some Requests options when calling `send`:

```python
client.send(req, verify=True, cert="/path/to/certificate",
            headers={"Content-Type": "application/json-rpc"})
```

As in the Requests library, any dictionaries passed to `send` in named
arguments will be merged with the session-level values that are set. The
method-level parameters override session parameters.

## Logging

Request and response messages are logged to the loggers
`jsonrpcclient.client.request` and `jsonrpcclient.client.response` on the INFO
log level.

```python
>>> client.request("ping")
--> {"jsonrpc": "2.0", "method": "ping", "id": 4}
<-- {"jsonrpc": "2.0", "result": "pong", "id": 4} (200 OK)
```

No handlers are created by default. Here's an example of adding handlers to
the loggers and setting the log level to INFO:

```python
from logging.config import dictConfig
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "request": {"format": "<-- %(message)s"},
        "response": {"format": "<-- %(message)s (%(http_code)s %(http_reason)s)"},
    },
    "handlers": {
        "request": {"formatter": "request", "class": "logging.StreamHandler"},
        "response": {"formatter": "response", "class": "logging.StreamHandler"},
    },
    "loggers": {
        "jsonrpcclient": {"level": "INFO"},
        "jsonrpcclient.client.request": {"handlers": ["request"]},
        "jsonrpcclient.client.response": {"handlers": ["response"]},
    },
}
dictConfig(log_config)
```

(For non-http clients, don't include http_code and http_reason in the
formats.)

For the lazy, you can pass `basic_logging=True` when creating the client
object, which will add a StreamHandler to each logger and set the log level to
INFO. (Alternatively call `client.basic_logging()`).
