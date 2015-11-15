Recent Changes
==============

2.1.0 (16 Nov 2015)
-------------------

- Send `batch requests
  <https://jsonrpcclient.readthedocs.org/http.html#batch-requests>`_.

- Send a raw JSON-RPC message with `send()
  <https://jsonrpcclient.readthedocs.org/http.html#usage>`_.

- The ``id`` part of requests can be `configured
  <https://jsonrpcclient.readthedocs.org/api.html#id-iterators>`_.

- Using the method name directly on the server object, e.g. ``server.cat()``, is
  now equal to ``server.request('cat')``. (Previously it was equal to
  ``server.notify('cat')``.)

- Removed ``ReceivedNoResponse`` and ``UnwantedException`` exceptions. The
  complexity of supporting them outweighed their usefulness.

- Project hosting has moved to `github <https://github.com/bcb/jsonrpcclient>`_.

2.0.1 (4 Sep 2015)
------------------

A major update, which makes way for protocols other than just HTTP.

- Importantly, the ``Server`` class has been renamed ``HTTPServer``. Adjust
  your code like this:

.. sourcecode:: python

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> server = HTTPServer('http://example.com/api')

- The requests module, which is required to send requests over HTTP, will no
  longer be installed as a dependency. It's now up to the user to install it
  like this:

.. sourcecode:: sh

    $ pip install jsonrpcclient requests

- Three exceptions have been removed: ``InvalidRequest`` (out of scope),
  ``InvalidResponse`` (catch ``jsonschema.ValidationError`` instead) and
  ``ConnectionError`` (catch the `requests module exceptions
  <http://www.python-requests.org/en/latest/api/#exceptions>`_ instead).

- Faster validation of response messages.

- Requests are now sent and logged with the JSON-RPC parts in the right order,
  (beginning with ``'jsonrpc': 2.0'`` etc.), which is just nicer to read.

- `ZeroMQ <http://jsonrpcclient.readthedocs.org/zeromq.html>`_ support
  added.

- `Documentation <http://jsonrpcclient.readthedocs.org/>`_ overhauled.
