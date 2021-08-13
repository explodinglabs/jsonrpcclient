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

.. literalinclude:: ../examples/http/request.py

ZeroMQ
------

.. code-block:: sh

    $ pip install 'jsonrpcclient[pyzmq]'

.. literalinclude:: ../examples/zeromq/request.py

See `blog post <https://blog.explodinglabs.com/jsonrpc/zeromq>`__.

Asynchronous
============

These require Python 3.5+.

aiohttp
-------

.. code-block:: sh

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp/request.py

See `blog post <https://blog.explodinglabs.com/jsonrpc/aiohttp>`__.

Tornado
-------

.. code-block:: sh

    $ pip install 'jsonrpcclient[tornado]'

.. literalinclude:: ../examples/tornado/request.py

Websockets
----------

.. code-block:: sh

    $ pip install 'jsonrpcclient[websockets]'

.. literalinclude:: ../examples/websockets/request.py

See `blog post <https://blog.explodinglabs.com/jsonrpc/websockets>`__.
