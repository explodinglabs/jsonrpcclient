jsonrpcclient
*************

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC
<http://www.jsonrpc.org/>`_.

Installation
============

.. code-block:: sh

    $ pip install jsonrpcclient

Usage
=====

Set the server details::

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> server = HTTPServer('http://example.com/api')

Make a request::

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
---------------

If you prefer, there's another way to make a request::

    >>> server.add(2, 3, response=True)
    5

That's the same as saying ``server.request('add', 2, 3)``. With this usage, pass
``response=True`` to get a response; without that it's a notification.

Exceptions
----------

Catch the base exception ``JsonRpcClientError`` in case there's a problem
communicating with the server::

    from jsonrpcclient.exceptions import ReceivedErrorResponse, JsonRpcClientError
    try:
        server.request('go')
    except JsonRpcClientError as e:
        print(str(e))

Here's the full list of exceptions, if you need to handle them individually:

ReceivedNoResponse
    A response message was expected, but none was given.

UnwantedResponse
    A response was not requested, but one was given anyway.

ParseResponseError
    The response was not valid JSON.

InvalidResponse
    The response was not a valid JSON-RPC response.

ReceivedErrorResponse
    The server gave a valid JSON-RPC error response.

If the server responds with a valid `JSON-RPC error object
<http://www.jsonrpc.org/specification#error_object>`_, the
``ReceivedErrorResponse`` exception has the details::

    from jsonrpcclient.exceptions import ReceivedErrorResponse, JsonRpcClientError
    try:
        server.request('go')
    except ReceivedErrorResponse as e:
        print(e.code, e.message, e.data)
    # Catch the base exception for other errors
    except JsonRpcClientError as e:
        print(str(e))

Logging
-------

To see the json messages being passed back and forth, set the log level to
INFO::

    import logging
    logging.basicConfig()
    logging.getLogger('jsonrpcclient').setLevel(logging.INFO)

For better logging, replace ``basicConfig`` with your own handlers, and
customize the log format for ``jsonrpcclient.server.request`` and
``jsonrpcclient.server.response``::

    request_handler = logging.StreamHandler()
    request_handler.setFormatter(logging.Formatter(fmt='%(endpoint)s --> %(message)s'))
    logging.getLogger('jsonrpcclient.server.request').addHandler(request_handler)

    response_handler = logging.StreamHandler()
    response_handler.setFormatter(logging.Formatter(fmt='%(endpoint)s <-- %(message)s'))
    logging.getLogger('jsonrpcclient.server.response').addHandler(response_handler)

The request format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://example.com/api``.

%(message)s
    The json request (the body).

The response format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://example.com/api``.

%(message)s
    The json response (the body).

More logging fields are available depending on your chosen transport method.

HTTPServer
==========

This section relates specifically to the HTTP transport protocol.

Authentication
--------------

To make authenticated requests, pass an ``auth`` argument to ``HTTPServer``::

    >>> server = HTTPServer('http://example.com/api', auth=('user', 'pass'))

For more authentication options, see the `requests module
<http://docs.python-requests.org/en/latest/user/authentication/>`_ which
handles the authentication.

Headers
-------

To customize the HTTP headers, pass a ``headers`` argument to ``HTTPServer``::

    >>> server = HTTPServer('http://example.com/api', headers={'Content-Type': 'application/json-rpc'})

If no headers are given, the following headers are used::

    Content-Type: application/json
    Accept: application/json

.. note::

    In addition to ``auth`` and ``headers``, other arguments can allow you to
    set the timeout, cookies, ssl verification and more. For the full list of
    options see the request method `here
    <https://github.com/kennethreitz/requests/blob/master/requests/api.py>`_.

Logging
-------

HTTPServer has the following extra logging fields.

The request format has these extra fields:

%(http_headers)s
    The full HTTP headers.

The response format has these extra fields:

%(http_code)d
    The HTTP status code received from the server, eg. ``400``.

%(http_reason)s
    The description of the status code, eg. ``BAD REQUEST``.

%(http_headers)s
    The full HTTP headers.

Todo
====

- Support `batch calls <http://www.jsonrpc.org/specification#batch>`_.
- More transport options.

Links
=====

- PyPi Package: https://pypi.python.org/pypi/jsonrpcclient
- Repository: https://bitbucket.org/beau-barker/jsonrpcclient
- Issue tracker: https://bitbucket.org/beau-barker/jsonrpcclient/issues

If you need a server, try my `jsonrpcserver
<https://jsonrpcserver.readthedocs.org/>`_ library.
