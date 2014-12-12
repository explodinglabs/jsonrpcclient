jsonrpcclient
=============

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC 2.0
<http://www.jsonrpc.org/>`_.

Installation
------------

    pip install jsonrpcclient

Usage
-----

.. sourcecode:: python

    >>> from jsonrpcclient import Server
    >>> server = Server('http://example/')
    >>> server.request('add', 2, 3)
    --> {"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
    <-- 200 {"jsonrpc": "2.0", "result": 5, "id": 1}
    5

.. hint::

    To see the underlying messages going back and forth, set the logging level
    to INFO:

    ``logging.getLogger('jsonrpcclient').setLevel(logging.INFO)``

The first argument to ``request()`` is the *method*; everything else is passed
as *params*. You can pass any number of positional or keyword arguments, and
they will be translated into JSON-RPC.

.. sourcecode:: python

    >>> server.request('find', 42, name='Foo')
    --> {"jsonrpc": "2.0", "method": "find", "params": [42, {"name": "Foo"}], "id": 1}
    <-- 200 {"jsonrpc": "2.0", "result": "Bar", "id": 1}
    Bar

.. note::
    To conform strictly to JSON-RPC 2.0 protocol, one should use either
    positional or keyword parameters, but not both in the same request. See
    `link
    <http://www.jsonrpc.org/specification#parameter_structures>`_.

If you don't need any data returned, use ``notify`` instead of ``request``.

.. sourcecode:: python

    >>> server.notify('go')
    --> {"jsonrpc": "2.0", "method": "go"}
    <-- 200 OK

Alternate usage
---------------

If you prefer, there's another way to call a remote procedure:

.. sourcecode:: python

    >>> server.add(2, 3, response=True)

Which is the same as saying ``server.request('add', 2, 3)``.

Use ``response=True`` to get a response; without that it's a notification.

Authentication
--------------

Make authenticated requests by passing a second argument to ``Server()``.

.. sourcecode:: python

    >>> server = Server('http://example/', auth=('user', 'pass'))

For more options, see the `requests
<http://docs.python-requests.org/en/latest/user/authentication/>`_ package
which handles the authentication.

Exceptions
----------

You should catch ``JsonRpcClientError``, which is the base exception. This will
be raised in the event of any issue that should be handled, such as connection
problems, or if the server responded with a *error* response.

.. sourcecode:: python

    from jsonrpcclient.exceptions import JsonRpcClientError
    try:
        server.go()
    except JsonRpcClientError as e:
        print(str(e))

Issue tracker is `here
<https://bitbucket.org/beau-barker/jsonrpcclient/issues>`_.

If you need a server, try my `jsonrpcserver
<https://pypi.python.org/pypi/jsonrpcserver>`_ library.

Todo
----

* Ability to make GET requests.

* Ability to configure the http header. Currently Content-Type is hard-coded as
  "application/json", but perhaps should be "application/json-rpc". See
  http://jsonrpc.org/historical/json-rpc-over-http.html#http-header


Changelog
---------

1.0.10 - 2014-12-11
    * Exceptions have been cleaned up. The base exception is now named
      ``JsonRpcClientError``.
    * Tests added for 100% code coverage.

1.0.9 - 2014-12-02
    * Added authentication.
    * Messages are now output on the INFO log level.

1.0.8 - 2014-12-02
    * Show the response status code in the log.

1.0.7 - 2014-11-21
    * When using the "alternate" (``server.add()``) method to make a request,
      only send "id" if response=True is explicitly passed (fixed)
    * The underlying JSON messages are now hidden by default. To see them you
      should increase the logging level (see above).
    * Tests moved into separate "tests" dir.

1.0.6 - 2014-11-11
    * Fixed installer.

1.0.5 - 2014-11-10
    * Better logging.

1.0.4 - 2014-11-10
    * "Proxy" class renamed to "Server".
    * Logging improved.
