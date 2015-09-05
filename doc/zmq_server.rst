jsonrpcclient: ZeroMQ
*********************

Make JSON-RPC requests over ZeroMQ.

Installation
============

.. code-block:: sh

    $ pip install jsonrpcclient pyzmq

Usage
=====

Set the server details::

    >>> from jsonrpcclient.zmq_server import ZMQServer
    >>> server = ZMQServer('tcp://localhost:5555')

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

zmq.ZMQError
    Error communicating with the server.

Logging
-------

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
    The server endpoint, eg. ``http://localhost:5555``.

%(message)s
    The JSON request (the body).

The response format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://localhost:5555``.

%(message)s
    The JSON response (the body).

Examples
========

- `JSON-RPC over ZeroMQ Client in Python <https://bitbucket.org/snippets/beau-barker/89AGe/json-rpc-over-zeromq-request-reply-client>`_

`Back home <index.html>`_
