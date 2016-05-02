jsonrpcclient
*************

Send JSON-RPC requests in Python 2.7 and 3.3+.

.. sourcecode:: python

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> HTTPServer('http://pets.com/api').request('cat')
    'meow'

Full documentation is at `jsonrpcclient.readthedocs.io
<https://jsonrpcclient.readthedocs.io/>`_.
