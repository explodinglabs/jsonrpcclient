.. rubric:: :doc:`index`

jsonrpcclient Guide
*******************

.. contents::
    :local:

Installation
============

Install jsonrpcclient with the *requests* library:

.. sourcecode:: sh

    $ pip install 'jsonrpcclient[requests]'

Import the ``HTTPClient`` class and instantiate it, passing the server
endpoint::

    >>> from jsonrpcclient.http_client import HTTPClient
    >>> client = HTTPClient('http://cats.com')

There are other :doc:`clients <examples>` available which use different
protocols to send a message. Regardless of the client, the rest of the usage
described below is the same.

Sending a request
=================

Send
----

Send a request, passing the whole JSON-RPC request object::

    >>> client.send('{"jsonrpc": "2.0", "method": "ping", "id": 1}')
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

Request
-------

Send a request by passing the method and arguments. This is the main public
method.

::

    >>> client.request('cat', name='Mittens')
    --> {"jsonrpc": "2.0", "method": "cat", "params": {"name": "Mittens"}, "id": 1}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
    'meow'

If you're not interested in a response, use ``notify()`` instead of
``request()``.

The Request class
=================

This class makes it easy to create a JSON-RPC `request object
<http://www.jsonrpc.org/specification#request_object>`_::

    >>> from jsonrpcclient.request import Request
    >>> Request('cat', name='Mittens')
    {'jsonrpc': '2.0', 'method': 'cat', 'params': {'name': 'Mittens'}, 'id': 1}

Send a ``Request`` object::

    >>> client.send(Request('ping'))
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

The :func:`~jsonrpcclient.client.Client.request` method above, is a wrapper
around ``send(Request())``.

If you're not interested in a response, use the ``Notification`` class instead
of ``Request``.

Batch requests
==============

JSON-RPC allows you to send multiple requests in a single message::

    client.send([
        {'jsonrpc': '2.0', 'method': 'cat', 'id': 1},
        {'jsonrpc': '2.0', 'method': 'dog', 'id': 2}])

Send multiple :class:`~jsonrpcclient.request.Request` objects::

    client.send([Request('cat'), Request('dog')])

Using list comprehension to get the cube of ten numbers::

    client.send([Request('cube', i) for i in range(10)])

Unlike single requests, batch requests return the whole JSON-RPC `batch
response <http://www.jsonrpc.org/specification#batch>`__ - a list of responses
for each request that had an ``id`` member.

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

As in the Requests library, any dictionaries passed to ``send`` in named
arguments will be merged with the session-level values that are set. The
method-level parameters override session parameters.
