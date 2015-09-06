jsonrpcclient
*************

Make `JSON-RPC <http://www.jsonrpc.org/>`_ requests in Python 2.7 and 3.3+.

Simply set the server details, then make a request:

.. sourcecode:: python

    >>> server = HTTPServer('http://example.com/api')
    >>> server.request('add', 2, 3)
    5

Full documentation is available at https://jsonrpcclient.readthedocs.org/.
