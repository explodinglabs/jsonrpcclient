jsonrpcclient: HTTP
*******************

Make JSON-RPC requests over HTTP.

Installation
============

.. code-block:: sh

    $ pip install jsonrpcclient requests

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

Exceptions
----------

Some exceptions one might encounter when making a request are:

jsonrpcclient.exceptions.ReceivedNoResponse
    A response message was expected, but none was given.

jsonrpcclient.exceptions.UnwantedResponse
    A response was not requested, but one was given.

jsonrpcclient.exceptions.ParseResponseError
    The response was not valid JSON.

jsonschema.ValidationError
    The response was not a valid JSON-RPC response object.

jsonrpcclient.exceptions.ReceivedErrorResponse
    The server gave a valid `JSON-RPC error response <http://www.jsonrpc.org/specification#error_object>`_.

The ``ReceivedErrorResponse`` exception has extra details, if you need it::

    from jsonrpcclient.exceptions import ReceivedErrorResponse
    try:
        server.request('go')
    except ReceivedErrorResponse as e:
        print(e.code, e.message, e.data)

Plus the `request module exceptions
<http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>`_.

Logging
=======

To see the JSON messages being passed back and forth, set the log level to
``INFO``::

    import logging
    logging.basicConfig()
    logging.getLogger('jsonrpcclient').setLevel(logging.INFO)

For better logging, customize the log format for
``jsonrpcclient.server.request`` and ``jsonrpcclient.server.response``::

    import logging
    logging.getLogger('jsonrpcclient').setLevel(logging.INFO)

    request_handler = logging.StreamHandler()
    request_handler.setFormatter(logging.Formatter(fmt='%(endpoint)s --> %(message)s'))
    logging.getLogger('jsonrpcclient.server.request').addHandler(request_handler)

    response_handler = logging.StreamHandler()
    response_handler.setFormatter(logging.Formatter(fmt='%(endpoint)s <-- %(message)s'))
    logging.getLogger('jsonrpcclient.server.response').addHandler(response_handler)

The request format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://example.com/api``.

%(http_headers)s
    The full HTTP headers.

%(message)s
    The JSON request (the body).

The response format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://example.com/api``.

%(http_code)d
    The HTTP status code received from the server, eg. ``400``.

%(http_reason)s
    The description of the status code, eg. ``BAD REQUEST``.

%(http_headers)s
    The full HTTP headers.

%(message)s
    The JSON response (the body).

Examples
========

- `JSON-RPC over HTTP Client in Python <https://bitbucket.org/snippets/beau-barker/KAjrB/json-rpc-over-http-client-in-python>`_

`Back home <index.html>`_
