jsonrpcclient
=============

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC
<http://www.jsonrpc.org/>`_.

Installation
------------

.. code-block:: sh

    $ pip install jsonrpcclient

Usage
-----

Set the server details, then make a request::

    >>> from jsonrpcclient import Server
    >>> server = Server('http://example.com/api')
    >>> server.request('add', 2, 3)
    5

The first argument to ``request`` is the *method*; everything else is passed as
*params*. Keyword arguments are also acceptable::

    >>> server.request('find', name='Foo', age=42)
    --> {"jsonrpc": "2.0", "method": "find", "params": {"name": "Foo", "age": 42}, "id": 1}
    <-- {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

.. tip::

    To see the underlying JSON messages going back and forth, see the Logging_
    section below.

If you don't need any data returned, use ``notify`` instead of ``request``::

    >>> server.notify('go')

Alternate usage
^^^^^^^^^^^^^^^

If you prefer, there's another way to make a request::

    >>> server.add(2, 3, response=True)
    5

That's the same as saying ``server.request('add', 2, 3)``. With this usage, pass
``response=True`` to get a response; without that it's a notification.

Authentication
^^^^^^^^^^^^^^

To make authenticated requests, pass an ``auth`` argument to ``Server``::

    >>> server = Server('http://example.com/api', auth=('user', 'pass'))

For more authentication options, see the `requests
<http://docs.python-requests.org/en/latest/user/authentication/>`_ module which
handles the authentication.

Headers
^^^^^^^

To customize the HTTP headers, pass a ``headers`` argument to ``Server``::

    >>> server = Server('http://example.com/api', headers={'Content-Type': 'application/json-rpc'})

If no headers are given, the following headers are used::

    Content-Type: application/json
    Accept: application/json

Exceptions
^^^^^^^^^^

Catch the base exception ``JsonRpcClientError`` in case there's a problem
communicating with the server::

    from jsonrpcclient.exceptions import JsonRpcClientError
    try:
        server.request('go')
    except JsonRpcClientError as e:
        print(str(e))

Here's the full list of exceptions, if you need to handle them individually:

InvalidRequest
    The request being sent is not valid json.

ConnectionError
    There was a network issue, invalid HTTP response or timeout.

Non200Response
    The server responded with a HTTP status code other than 200.

ParseResponseError
    The response was not valid json.

InvalidResponse
    The response didnt validate against the json-rpc response schema.

ReceivedNoResponse
    A response was expected, but none was given.

UnwantedResponse
    A response was not requested, but was given anyway.

ReceivedErrorResponse
    The server gave a valid JSON-RPC *error* response.

Logging
^^^^^^^

To give fine control, two loggers are used; ``request_log`` for requests and
``response_log`` for responses. These do nothing until they're set up. The
following shows how to output the ``request_log`` to stderr::

    from logging import StreamHandler, Formatter, INFO
    from jsonrpcclient import request_log, response_log

    # Json messages are on the INFO log level.
    request_log.setLevel(INFO)

    # Add a stream handler to output to stderr.
    request_handler = StreamHandler()
    request_log.addHandler(request_handler)

Do the same with ``response_log`` to see the responses::

    response_log.setLevel(INFO)
    response_handler = StreamHandler()
    response_log.addHandler(response_handler)

For better log entries, customize the log format::

    # Set a custom request log format
    request_format = Formatter(fmt='--> %(message)s')
    request_handler.setFormatter(request_format)

    # Set a custom response log format
    response_format = Formatter(fmt='<-- %(http_code)d %(http_reason)s %(message)s')
    response_handler.setFormatter(response_format)

In the response format, these extra fields can be used:

%(http_code)
    The HTTP status code received from the server, eg. *400*.

%(http_reason)
    The description of the status code, eg. *"BAD REQUEST"*.

Todo
----

* Support `batch calls <http://www.jsonrpc.org/specification#batch>`_.
* Ability to make GET requests - maybe.

Links
-----

* Package: https://pypi.python.org/pypi/jsonrpcclient
* Repository: https://bitbucket.org/beau-barker/jsonrpcclient
* Issue tracker: https://bitbucket.org/beau-barker/jsonrpcclient/issues

If you need a server, try my `jsonrpcserver
<http://jsonrpcserver.readthedocs.org/>`_ library.
