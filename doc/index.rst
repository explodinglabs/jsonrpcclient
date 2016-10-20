.. rubric:: `Beau Barker <https://bcb.github.io/>`__

jsonrpcclient
*************

Send `JSON-RPC <http://www.jsonrpc.org/>`__ requests in Python 2.7 and 3.3+.

.. sourcecode:: sh

    $ pip install 'jsonrpcclient[requests]'

.. sourcecode:: python

    >>> from jsonrpcclient.http_client import HTTPClient
    >>> HTTPClient('http://cats.com/').request('speak')
    --> {"jsonrpc": "2.0", "method": "speak", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "meow", "id": 1}
    'meow'

This example uses the *requests* library for sending, but more options are
available. See :doc:`examples in various frameworks <examples>`, or read the
:doc:`guide to usage and configuration<api>`.

Contribute on `Github <https://github.com/bcb/jsonrpcclient>`__.

See also: `jsonrpcserver <https://jsonrpcserver.readthedocs.io/>`__
