Release History
===============

2.0.1 (2015-09-04)
------------------

A major update.

- The ``Server`` class has been renamed ``HTTPServer``. This is in order to make
  way for more transport options.

Adjust your code like this:

.. sourcecode:: python

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> server = HTTPServer('http://example.com/api')

- The ``InvalidRequest`` exception has been removed. Invalid requests will be
  handled appropriately by the server. It's not the responsibility of this
  library to catch invalid requests.

- The ``ConnectionError`` exception has been removed, because it only served to
  squash other more meaningful exceptions raised by the transport libraries. For
  example if you're working with ``HTTPServer`` which uses the requests module,
  catch the `requests module exceptions
  <http://www.python-requests.org/en/latest/api/#exceptions>`_ instead of
  ``ConnectionError``.

1.1.8 (2015-08-01)
------------------

- Further details provided when the server responds with a JSON-RPC error
  response. See `Exceptions
  <http://jsonrpcclient.readthedocs.org/#exceptions>`_.

1.1.7 (2015-05-20)
------------------

- Include the server endpoint in log entries.
