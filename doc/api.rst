.. rubric:: :doc:`index`

jsonrpcclient API
*****************

Request
=======

.. automethod:: jsonrpcclient.client.Client.request

If you're not interested in a response, use ``notify()`` instead of
``request()``.

Send
====

.. automethod:: jsonrpcclient.client.Client.send

Request class
=============

::

    from jsonrpcclient import Request

.. autoclass:: jsonrpcclient.request.Request

Send a ``Request`` object::

    >>> client.send(Request('ping'))
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

The :func:`~jsonrpcclient.client.Client.request` method is a wrapper around
``send(Request())``.

If you're not interested in a response, use the ``Notification`` class instead
of ``Request``.

Batch requests
==============

This JSON-RPC feature allows you to send multiple requests in a single
message::

    client.send([
        {'jsonrpc': '2.0', 'method': 'cat', 'id': 1},
        {'jsonrpc': '2.0', 'method': 'dog', 'id': 2}])

Send multiple :class:`~jsonrpcclient.request.Request` objects::

    client.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    client.send([Request('cube', i) for i in range(10)])

Unlike single requests, batch requests return the whole JSON-RPC response
object - a list of responses for each request that had an ``id`` member.

*The server may not support batch requests.*

Configuration
=============

.. automodule:: jsonrpcclient.config

Configuring the Requests library
--------------------------------

HTTPClient makes use of Kenneth Reitz's Requests library. The `Session
<http://docs.python-requests.org/en/master/api/#requests.Session>`_ is
available so you can configure it before sending any requests.

For example, Basic Auth::

    client.session.auth = ('user', 'pass')

SSL authentication::

    client.session.verify = '/path/to/certificate'

Custom HTTP headers::

    client.session.headers.update({'Content-Type': 'application/json-rpc'})

You can also configure some Requests options when calling
:func:`~jsonrpcclient.client.Client.send`::

    client.send(req, verify=True, cert='/path/to/certificate',
                headers={'Content-Type': 'application/json-rpc'})

As in the Requests library, any dictionaries passed to send in named arguments
will be merged with the session-level values that are set. The method-level
parameters override session parameters.
