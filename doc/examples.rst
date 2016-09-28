.. rubric:: :doc:`index`

jsonrpcclient Examples
**********************

Showing how to send JSON-RPC requests using various frameworks and transport
protocols.

.. contents::
    :local:

aiohttp
=======

``aiohttpClient`` uses the `aiohttp <http://aiohttp.readthedocs.io/>`__
library::

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp_client.py

Requests
========

``HTTPClient`` uses the `Requests <http://docs.python-requests.org/>`__ library.

::

    $ pip install 'jsonrpcclient[requests]'

.. literalinclude:: ../examples/http_client.py

Tornado
=======

``TornadoClient`` uses `Tornado <http://www.tornadoweb.org/>`__ to send an
asynchronous request.

::

    $ pip install 'jsonrpcclient[tornado]'

.. literalinclude:: ../examples/tornado_client.py

Note the ``async``/``await`` syntax requires Python 3.5+. Prior to that use
`@gen.coroutine and yield
<http://tornado.readthedocs.io/en/stable/guide/coroutines.html#python-3-5-async-and-await>`__.

See `blog post <https://bcb.github.io/jsonrpc/tornado>`__.

Websockets
==========

``WebSocketsClient`` uses the `websockets <http://websockets.readthedocs.io/>`__
library::

    $ pip install 'jsonrpcclient[aiohttp]'

.. literalinclude:: ../examples/aiohttp_client.py

ZeroMQ
======

``ZeroMQClient`` uses `pyzmq <https://pyzmq.readthedocs.io/>`__ for comms with
a ZeroMQ server.

::

    $ pip install 'jsonrpcclient[pyzmq]'

.. literalinclude:: ../examples/zeromq_client.py

See `blog post <https://bcb.github.io/jsonrpc/zeromq>`__.
