.. rubric:: :doc:`index`

jsonrpcclient Examples
**********************

Sending JSON-RPC requests in Python using various frameworks and transport
protocols.

Requests
========

Uses the `Requests <http://docs.python-requests.org/>`__ library.

::

    $ pip install jsonrpcclient requests

::

    >>> from jsonrpcclient.http_client import HTTPClient
    >>> HTTPClient('http://localhost:5000/').request('ping')
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

ZeroMQ
======

Uses `pyzmq <https://pyzmq.readthedocs.io/>`__.

::

    $ pip install jsonrpcclient pyzmq

::

    >>> from jsonrpcclient.zmq_client import ZMQClient
    >>> ZMQClient('tcp://localhost:5000').request('ping')
    --> {"jsonrpc": "2.0", "method": "ping", "id": 1}
    <-- {"jsonrpc": "2.0", "result": "pong", "id": 1}
    'pong'

See `blog post <https://bcb.github.io/jsonrpc/pyzmq>`__.

Tornado
=======

`Tornado <http://www.tornadoweb.org/>`__ users can send an asynchronous
request.

::

    $ pip install jsonrpcclient tornado

::

    from tornado import gen, ioloop
    from jsonrpcclient.tornado_client import TornadoClient

    client = TornadoClient('http://localhost:5000/')

    def done_callback(future):
        print(future.result())

    @gen.coroutine
    def main():
        future = client.request('ping')
        future.add_done_callback(done_callback)
        yield(future)

    io_loop = ioloop.IOLoop.current().run_sync(main)

::

    $ python client.py
    INFO:jsonrpcclient.client.request:{"jsonrpc": "2.0", "method": "ping", "id": 1}
    INFO:jsonrpcclient.client.response:{"jsonrpc": "2.0", "result": "pong", "id": 1}
    pong

See `blog post <https://bcb.github.io/jsonrpc/tornado>`__.
