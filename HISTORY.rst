Release History
===============

2.0.1 (2015-09-04)
------------------

A major update. These changes will open up the module for using communication
protocols other than just HTTP.

- Most importantly, the ``Server`` class has been renamed ``HTTPServer``.
  Adjust your code like this:

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

- Requests are sent and logged with the JSON-RPC parts in the right order,
  (beginning with ``'jsonrpc': 2.0'`` etc.), which is just nicer to read.

- Other fixes and improvements.

1.1.8 (2015-08-01)
------------------

- Further details provided when the server responds with a JSON-RPC error
  response. See `Exceptions
  <http://jsonrpcclient.readthedocs.org/#exceptions>`_.

1.1.7 (2015-05-20)
------------------

- Include the server endpoint in log entries.
