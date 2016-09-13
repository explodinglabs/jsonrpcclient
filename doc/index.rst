jsonrpcclient
*************

Send `JSON-RPC <http://www.jsonrpc.org/>`__ requests in Python 2.7 and 3.3+.

.. sourcecode:: sh

    $ pip install jsonrpcclient requests

.. sourcecode:: python

    >>> from jsonrpcclient.http_client import HTTPClient
    >>> HTTPClient('http://cats.com/').request('speak')
    --> {"jsonrpc": "2.0", "method": "speak", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
    'meow'

This example uses `Requests <http://docs.python-requests.org/>`__ library to
send a request. More options are demonstrated on the :doc:`examples <examples>`
page. For advanced usage and configuration, see the :doc:`api`.

Contribute on `Github <https://github.com/bcb/jsonrpcclient>`__.

See also: `jsonrpcserver.readthedocs.io <https://jsonrpcserver.readthedocs.io/>`__
