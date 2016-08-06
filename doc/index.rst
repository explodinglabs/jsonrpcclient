jsonrpcclient
*************

Send `JSON-RPC <http://www.jsonrpc.org/>`__ requests in Python 2.7 and 3.3+.

.. sourcecode:: sh

    $ pip install jsonrpcclient requests

.. sourcecode:: python

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> HTTPServer('http://pets.com').request('cat', name='Mittens')
    --> {"jsonrpc": "2.0", "method": "cat", {"params": {"name": "Mittens"}, "id": 1}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
    'meow'

For lower-level functions and configuration options, see the :doc:`guide`.

Contribute on `Github <https://github.com/bcb/jsonrpcserver>`_.

See also: `jsonrpcserver <https://jsonrpcserver.readthedocs.io/>`_
