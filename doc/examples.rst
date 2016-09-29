.. rubric:: :doc:`index`

jsonrpcclient Examples
**********************

Showing how to send JSON-RPC requests using various frameworks and transport
protocols.

.. contents::
    :local:

Synchronous
===========

Requests
--------

Uses `requests <http://docs.python-requests.org/>`__.

.. code-block:: sh

    $ pip install 'jsonrpcclient[requests]'

.. literalinclude:: ../examples/http_client.py

ZeroMQ
------

Uses `pyzmq <https://pyzmq.readthedocs.io/>`__.

.. code-block:: sh

    $ pip install 'jsonrpcclient[pyzmq]'

.. literalinclude:: ../examples/zeromq_client.py

See `blog post <https://bcb.github.io/jsonrpc/zeromq>`__.

Asynchronous
============

These require Python 3.5+.

aiohttp
-------

Uses `aiohttp <http://aiohttp.readthedocs.io/>`__.

.. code-block:: sh

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp_client.py

See `blog post <https://bcb.github.io/jsonrpc/aiohttp>`__.

Tornado
-------

Uses `Tornado <http://www.tornadoweb.org/>`__.

.. code-block:: sh

    $ pip install 'jsonrpcclient[tornado]'

.. literalinclude:: ../examples/tornado_client.py

See `blog post <https://bcb.github.io/jsonrpc/tornado>`__.

Websockets
----------

Uses `websockets <http://websockets.readthedocs.io/>`__.

.. code-block:: sh

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp_client.py

ZeroMQ (async)
--------------

Uses `pyzmq <https://pyzmq.readthedocs.io/>`__.

.. code-block:: sh

    $ pip install 'jsonrpcclient[pyzmq]'

.. literalinclude:: ../examples/zeromq_client.py

See `blog post <https://bcb.github.io/jsonrpc/zeromq>`__.
