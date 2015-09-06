Recent Changes
==============

2.0.1 (2015-09-04)
------------------

A major update. These changes open up the module for communication protocols
other than just HTTP.

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

- `ZeroMQ <http://jsonrpcclient.readthedocs.org/zeromq.html>`_ protocol
  added.

- `Documentation <http://jsonrpcclient.readthedocs.org/>`_ overhauled.

- Other fixes and improvements.
