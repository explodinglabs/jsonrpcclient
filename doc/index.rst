jsonrpcclient
=============

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC
<http://www.jsonrpc.org/>`_.

..
    Compliant with the `JSON-RPC 2.0 specification
    <http://www.jsonrpc.org/specification>`_ and `RFC 4627
    <http://tools.ietf.org/html/rfc4627>`_ on Javascript Object Notation.

Installation
------------

.. code-block:: sh

    $ pip install jsonrpcclient

Usage
-----

Set the server details, then make a request.

.. code-block:: python

    >>> from jsonrpcclient import Server
    >>> server = Server('http://example.com/api')
    >>> server.request('add', 2, 3)
    5

The first argument to ``request`` is the *method*; everything else is passed as
*params*. You can can also use keyword arguments.

.. code-block:: python

    >>> server.request('find', name='Foo', age=42)
    --> {"jsonrpc": "2.0", "method": "find", "params": {"name": "Foo", "age": 42}, "id": 1}
    <-- {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

.. tip::

    To see the underlying JSON messages going back and forth, see the Logging_
    section below.

..
    To comply strictly with the JSON-RPC 2.0 protocol, one should use *either*
    positional or keyword arguments, but not both in the same request. See
    `Parameter Structures
    <http://www.jsonrpc.org/specification#parameter_structures>`_.

If you don't need any data returned, use ``notify`` instead of ``request``.

.. code-block:: python

    >>> server.notify('go')
    >>>

Alternate usage
~~~~~~~~~~~~~~~

If you prefer, there's another way to make a request:

.. code-block:: python

    >>> server.add(2, 3, response=True)
    5

That's the same as saying ``server.request('add', 2, 3)``. Use
``response=True`` to get a response; without that it's a notification.

Authentication
--------------

To make authenticated requests, pass an ``auth`` argument to ``Server``.

.. code-block:: python

    >>> server = Server('http://example.com/api', auth=('user', 'pass'))

For more authentication options, see the `requests
<http://docs.python-requests.org/en/latest/user/authentication/>`_ module which
handles the authentication.

Headers
-------

To customize the HTTP headers, pass a ``headers`` argument to ``Server``.

.. code-block:: python

    >>> server = Server('http://example.com/api', headers={'Content-Type': 'application/json-rpc'})

If no custom headers are specified, the following headers are used::

    Content-Type: application/json
    Accept: application/json

Exceptions
----------

Catch the base exception ``JsonRpcClientError`` when communicating with the
server. This is raised on a variety of issues such as connection problems, or
if the server responded with *error*.

.. code-block:: python

    from jsonrpcclient.exceptions import JsonRpcClientError
    try:
        server.request('go')
    except JsonRpcClientError as e:
        print(str(e))

Logging
-------

To give finer control, two separate loggers are used - one for requests and
another for responses. These do nothing until you set them up and add handlers
to them.

The following shows how to output requests to stderr.

.. code-block:: python

    import logging
    from jsonrpcclient import request_log
    # Json messages are logged with info(), so set the log level.
    request_log.setLevel(logging.INFO)
    # Add a stream handler to output to stderr.
    request_handler = logging.StreamHandler()
    request_log.addHandler(request_handler)

Do the same with ``response_log`` to see the responses.

.. code-block:: python

    from jsonrpcclient import response_log
    response_log.setLevel(logging.INFO)
    response_handler = logging.StreamHandler()
    response_log.addHandler(response_handler)

For better log entries, customize the log format:

.. code-block:: python

    request_format = logging.Formatter(fmt='%(asctime)s --> %(message)s')
    request_handler.setFormatter(request_format)

    response_format = logging.Formatter(fmt='%(asctime)s <-- %(http_code)d %(http_reason)s %(message)s')
    response_handler.setFormatter(response_format)

In the response format, these extra fields can be used:

* ``%(http_code)`` is the HTTP status code received from the server (eg. *400*)
* ``%(http_reason)`` is the description of the status code (eg. *"BAD REQUEST"*)

Links
-----

Documentation: http://jsonrpcclient.readthedocs.org/
Package: https://bitbucket.org/beau-barker/jsonrpcclient/issues
Repository: https://bitbucket.org/beau-barker/jsonrpcclient/issues
Issue tracker: https://bitbucket.org/beau-barker/jsonrpcclient/issues

If you need a server, try my `jsonrpcserver
<https://pypi.python.org/pypi/jsonrpcserver>`_ library.

Todo
----

* Support `batch calls <http://www.jsonrpc.org/specification#batch>`_.
* Ability to make GET requests - maybe.

Changelog
---------

1.0.12 - 2014-12-16
    * Default HTTP headers changed to meet `this document
      <http://www.simple-is-better.org/json-rpc/transport_http.html#post-request>`_.
    * Ability customize the headers.
    * Logging has changed. See Logging_.

1.0.11 - 2014-12-12
    * Rewrote an internal function, ``rpc.request``.

1.0.10 - 2014-12-11
    * Exceptions have been cleaned up. The base exception is now named
      ``JsonRpcClientError``.
    * Tests added for 100% code coverage.

1.0.9 - 2014-12-02
    * Added authentication.
    * Messages are now output on the INFO log level.

1.0.8 - 2014-12-02
    * Show the response status code in the log.
