.. rubric:: :doc:`index`

jsonrpcclient Guide
*******************

An explanation of the developer interface, as well as :mod:`configuration
<config>`_ and some of the more advanced features of the library.

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

.. automodule:: config

ID Generators
-------------

.. automodule:: id_iterators

Requests configuration
----------------------

The `Requests
<http://docs.python-requests.org/en/master/api/#requests.Session>`_ module’s
Session is available so you can configure that before sending any requests.

For example, for SSL authentication:

    >>> server.session.verify = '/path/to/cert'

Basic Auth:

    >>> server.session.auth = ('user', 'pass')

Custom HTTP headers:

    >>> server.session.headers.update({'Content-Type': 'application/json-rpc'})

You can also configure the Request options when calling send:

>>> server.send(req, auth=('user', 'pass'))
>>> server.send(req, headers={'Content-Type': 'application/json-rpc'})

As in the requests library, any dictionaries passed to send in named arguments
will be merged with the session-level values that are set. The method-level
parameters override session parameters.
