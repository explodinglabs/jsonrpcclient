jsonrpcclient over ZeroMQ
*************************

Send JSON-RPC requests over ZeroMQ.

Installation
============

.. code-block:: sh

    $ pip install jsonrpcclient pyzmq

Usage
=====

Set the server details::

    from jsonrpcclient.zmq_server import ZMQServer
    server = ZMQServer('tcp://localhost:5555')

.. include:: _includes/making_a_request.rst

Exceptions
==========

In the event of a communications problem, pyzmq raises `zmq.ZMQError
<https://zeromq.github.io/pyzmq/pyversions.html#exceptions>`_::

    try:
        server.notify('go')
    except zmq.ZMQError as e:
        print(str(e))

.. include:: _includes/standard_exceptions.rst

Logging
=======

.. include:: _includes/basic_logging.rst

Or use custom handlers and formats::

    request_format = '%(endpoint)s --> %(message)s'
    response_format = '%(endpoint)s <-- %(message)s'

    request_handler = logging.StreamHandler()
    request_handler.setFormatter(logging.Formatter(fmt=request_format))
    logging.getLogger('jsonrpcclient.server.request').addHandler(
        request_handler)

    response_handler = logging.StreamHandler()
    response_handler.setFormatter(logging.Formatter(fmt=response_format))
    logging.getLogger('jsonrpcclient.server.response').addHandler(
        response_handler)

The request format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://localhost:5555``.

%(message)s
    The JSON request (the body).

The response format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://localhost:5555``.

%(message)s
    The JSON response (the body).

Examples
========

- `ZeroMQ Client
  <https://bitbucket.org/snippets/beau-barker/89AGe/json-rpc-over-zeromq-request-reply-client>`_
  using PyZMQ

`Back home <index.html>`_
