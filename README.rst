jsonrpcclient
*************

Send JSON-RPC requests in Python 2.7 and 3.3+.

.. sourcecode:: python

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> HTTPServer('http://cats.com/').request('speak')
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

Full documentation is at `jsonrpcclient.readthedocs.io
<https://jsonrpcclient.readthedocs.io/>`_.
