jsonrpcclient
*************

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC
<http://www.jsonrpc.org/>`_.

.. sourcecode:: sh

    $ pip install jsonrpcclient requests

Simply set the server details, then make a request:

.. sourcecode:: python

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> server = HTTPServer('http://example.com/api')
    >>> server.request('add', 2, 3)
    5

Full documentation is available at https://jsonrpcclient.readthedocs.org/.
