jsonrpcclient
*************

Send `JSON-RPC <http://www.jsonrpc.org/>`__ requests in Python 2.7 and 3.3+.

.. sourcecode:: python

    >>> from jsonrpcclient.http_client import HTTPClient
    >>> HTTPClient('http://cats.com/').request('speak')
    --> {"jsonrpc": "2.0", "method": "speak", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
    'meow'

Full documentation is at `jsonrpcclient.readthedocs.io
<https://jsonrpcclient.readthedocs.io/>`__.
