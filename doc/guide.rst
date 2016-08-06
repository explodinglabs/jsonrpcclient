.. rubric:: :doc:`index`

jsonrpcclient Guide
*******************

Send
====

Send a JSON-RPC message with ``send()``:

.. automethod:: server.Server.send

Request class
=============

The ``Request`` class makes it easy to create a JSON-RPC message::

    >>> from jsonrpcclient import Request

.. autoclass:: request.Request

Send a ``Request`` object::

    >>> server.send(Request('cat'))
    --> {"jsonrpc": "2.0", "method": "cat", "id": 1}

If you're not interested in a response, use ``Notification`` instead of
``Request``.

Request method
==============

This is just a wrapper around ``send(Request())``.

.. automethod:: server.Server.request

If you're not interested in a response, use ``notify()`` instead of
``request()``.

Batch Requests
==============

This feature of JSON-RPC allows you to send multiple requests in a single
message::

    >>> server.send([{'jsonrpc': '2.0', 'method': 'cat'}, {'jsonrpc': '2.0', 'method': 'dog'}])

Send multiple ``Request`` objects::

    >>> server.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    >>> server.send([Request('cube', i) for i in range(10)])

Unlike single requests, batch requests return the whole JSON-RPC response
object, i.e. a list of responses for each request that had an ``id`` member.

*The server may not support batch requests.*

Configuration
=============

Config module
Requests configuration
Id configuration
