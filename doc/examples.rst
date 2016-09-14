.. rubric:: :doc:`index`

jsonrpcclient Examples
**********************

Sending JSON-RPC requests in Python using various frameworks and transport
protocols.

.. contents::
    :local:

Requests
========

``HTTPClient`` uses the `Requests <http://docs.python-requests.org/>`__ library.

::

    $ pip install jsonrpcclient requests

::

    >>> from jsonrpcclient.http_client import HTTPClient
    >>> HTTPClient('http://localhost:5000/').request('ping')
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

Tornado
=======

``TornadoClient`` uses `Tornado <http://www.tornadoweb.org/>`__ to send an
asynchronous request.

::

    $ pip install jsonrpcclient tornado

::

    from tornado import ioloop
    from jsonrpcclient.tornado_client import TornadoClient

    client = TornadoClient('http://localhost:5000/')

    def done_callback(future):
        print(future.result())

    async def main():
        future = client.request('ping')
        future.add_done_callback(done_callback)
        await future

    io_loop = ioloop.IOLoop.current().run_sync(main)

Note the ``async``/``await`` syntax requires Python 3.5+. Prior to that use
`@gen.coroutine and yield
<http://tornado.readthedocs.io/en/stable/guide/coroutines.html#python-3-5-async-and-await>`__.

::

    $ python client.py
    INFO:jsonrpcclient.client.request:{"jsonrpc": "2.0", "method": "ping", "id": 1}
    INFO:jsonrpcclient.client.response:{"jsonrpc": "2.0", "result": "pong", "id": 1}
    pong

See `blog post <https://bcb.github.io/jsonrpc/tornado>`__.

ZeroMQ
======

``ZMQClient`` uses `pyzmq <https://pyzmq.readthedocs.io/>`__ for comms with a
ZeroMQ server.

::

    $ pip install jsonrpcclient pyzmq

::

    >>> from jsonrpcclient.zmq_client import ZMQClient
    >>> ZMQClient('tcp://localhost:5000').request('ping')
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

See `blog post <https://bcb.github.io/jsonrpc/pyzmq>`__.
