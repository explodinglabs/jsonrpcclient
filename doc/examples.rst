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

.. code-block:: sh

    $ pip install 'jsonrpcclient[requests]'

.. literalinclude:: ../examples/http_client.py

ZeroMQ
------

.. code-block:: sh

    $ pip install 'jsonrpcclient[pyzmq]'

.. literalinclude:: ../examples/zeromq_client.py

See `blog post <https://bcb.github.io/jsonrpc/zeromq>`__.

Asynchronous
============

These require Python 3.5+.

aiohttp
-------

.. code-block:: sh

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp_client.py

See `blog post <https://bcb.github.io/jsonrpc/aiohttp>`__.

Tornado
-------

.. code-block:: sh

    $ pip install 'jsonrpcclient[tornado]'

.. literalinclude:: ../examples/tornado_client.py

See `blog post <https://bcb.github.io/jsonrpc/tornado>`__.

Websockets
----------

.. code-block:: sh

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp_client.py

ZeroMQ (async)
--------------

.. code-block:: sh

    $ pip install 'jsonrpcclient[pyzmq]'

.. literalinclude:: ../examples/zeromq_client.py

See `blog post <https://bcb.github.io/jsonrpc/zeromq>`__.
