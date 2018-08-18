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

    $ pip install "jsonrpcclient[requests]"

.. literalinclude:: ../examples/http/single.py

ZeroMQ
------

.. code-block:: sh

    $ pip install 'jsonrpcclient[pyzmq]'

.. literalinclude:: ../examples/zeromq/single.py

See `blog post <https://bcb.github.io/jsonrpc/zeromq>`__.

Asynchronous
============

These require Python 3.5+.

aiohttp
-------

.. code-block:: sh

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp/single.py

See `blog post <https://bcb.github.io/jsonrpc/aiohttp>`__.

Tornado
-------

.. code-block:: sh

    $ pip install 'jsonrpcclient[tornado]'

.. literalinclude:: ../examples/tornado/single.py

Websockets
----------

.. code-block:: sh

    $ pip install 'jsonrpcclient[websockets]'

.. literalinclude:: ../examples/websockets/single.py

See `blog post <https://bcb.github.io/jsonrpc/websockets>`__.
