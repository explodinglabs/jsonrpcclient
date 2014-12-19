jsonrpcclient
=============

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC
<http://www.jsonrpc.org/>`_.

Compliant with the `JSON-RPC 2.0 specification
<http://www.jsonrpc.org/specification>`_ and `RFC 4627
<http://tools.ietf.org/html/rfc4627>`_ on JSON notation.

.. sourcecode:: python

    >>> from jsonrpcclient import Server
    >>> server = Server('http://example.com/api')
    >>> server.request('add', 2, 3)
    5

Installation
------------

.. sourcecode:: sh

    $ pip install jsonrpcclient

Documentation
-------------

Documentation is available at http://jsonrpcclient.readthedocs.org/.

Server
------

If you need a server, try my `jsonrpcserver
<https://jsonrpcserver.readthedocs.org/>`_ library.
