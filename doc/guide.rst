.. rubric:: :doc:`index`

jsonrpcclient API
*****************

Some of the more advanced features of the library, including usage and
:mod:`configuration <config>`.

Request
=======

.. automethod:: server.Server.request

If you're not interested in a response, use ``notify()`` instead of
``request()``.

Send
====

.. automethod:: server.Server.send

Request class
=============

>>> from jsonrpcclient import Request

.. autoclass:: request.Request

Send a ``Request`` object::

    >>> server.send(Request('ping'))
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

The :func:`~server.Server.request` method is a wrapper around
``send(Request())``.

If you're not interested in a response, use ``Notification`` instead of
``Request``.

Batch requests
==============

This JSON-RPC feature allows you to send multiple requests in a single
message::

    >>> server.send([
    ...     {'jsonrpc': '2.0', 'method': 'cat', 'id': 1}, \
    ...     {'jsonrpc': '2.0', 'method': 'dog', 'id': 2}])

Send multiple ``Request`` objects::

    >>> server.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    >>> server.send([Request('cube', i) for i in range(10)])

Unlike single requests, batch requests return the whole JSON-RPC response
object - a list of responses for each request that had an ``id`` member.

*The server may not support batch requests.*

Configuration
=============

.. automodule:: config

ID Generators
-------------

.. automodule:: id_iterators

Configuring the Requests library
--------------------------------

The HTTPServer class makes use of python's Requests library. The `Session
<http://docs.python-requests.org/en/master/api/#requests.Session>`_ is
available so you can configure that before sending any requests.

For example, for SSL authentication::

    >>> server.session.verify = '/path/to/certificate'

Basic Auth::

    >>> server.session.auth = ('user', 'pass')

Custom HTTP headers::

    >>> server.session.headers.update({'Content-Type': 'application/json-rpc'})

You can also configure some Requests options when calling
:func:`~server.Server.send`::

    >>> server.send(req, verify=True, cert='/path/to/certificate')

As in the Requests library, any dictionaries passed to send in named arguments
will be merged with the session-level values that are set. The method-level
parameters override session parameters.
