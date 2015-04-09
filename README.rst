jsonrpcclient
=============

.. image:: https://pypip.in/v/jsonrpcclient/badge.png
.. image:: https://pypip.in/d/jsonrpcclient/badge.png

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC
<http://www.jsonrpc.org/>`_.

Simply set the server details, then make a request:

.. sourcecode:: python

    >>> Server('http://example.com/api').request('add', 2, 3)
    5

Full documentation is available at https://jsonrpcclient.readthedocs.org/.
