jsonrpcclient
*************

Send `JSON-RPC <http://www.jsonrpc.org/>`__ requests in Python 2.7 and 3.3+.

.. sourcecode:: sh

    $ pip install jsonrpcclient requests

.. sourcecode:: python

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> HTTPServer('http://cats.com/').request('speak')
    --> {"jsonrpc": "2.0", "method": "speak", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
    'meow'

For advanced usage and configuration, see the :doc:`api`.

Contribute on `Github <https://github.com/bcb/jsonrpcserver>`_.

See also: `jsonrpcserver <https://jsonrpcserver.readthedocs.io/>`_
