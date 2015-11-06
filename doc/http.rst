.. rubric::
    `jsonrpcclient <index.html>`_

jsonrpcclient over HTTP
***********************

Send JSON-RPC requests over HTTP.

Installation
============

.. code-block:: sh

    $ pip install jsonrpcclient requests

Usage
=====

Set the server details::

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> server = HTTPServer('http://pets.com/api')

.. include:: _includes/requests.rst

Headers
-------

To customize the HTTP headers, pass a ``headers`` argument to ``HTTPServer``::

    >>> server = HTTPServer('http://example.com/api', headers={'Content-Type': 'application/json-rpc'})

If no headers are given, the following headers are used::

    Content-Type: application/json
    Accept: application/json

Authentication
--------------

To make authenticated requests, pass an ``auth`` argument to ``HTTPServer``::

    >>> server = HTTPServer('http://example.com/api', auth=('user', 'pass'))

For more authentication options, see the `requests module
<http://docs.python-requests.org/en/latest/user/authentication/>`_ which
handles the authentication.

.. note::

    In addition to ``auth`` and ``headers``, other arguments can allow you to
    set the timeout, cookies, SSL verification and more. For the full list of
    options see the request method `here
    <https://github.com/kennethreitz/requests/blob/master/requests/api.py>`__.

Exceptions
==========

In the event of a communications problem, the Requests module raises
`requests.exceptions.RequestException <http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>`_::

    try:
        server.request('go')
    except requests.exceptions.RequestException as e:
        print(str(e))

.. include:: _includes/exceptions.rst

Logging
=======

.. include:: _includes/logging.rst

The request format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://example.com/api``.

%(http_headers)s
    The full HTTP headers.

%(message)s
    The JSON request (the body).

The response format has these fields:

%(endpoint)s
    The server endpoint, eg. ``http://example.com/api``.

%(http_code)d
    The HTTP status code received from the server, eg. ``400``.

%(http_reason)s
    The description of the status code, eg. ``BAD REQUEST``.

%(http_headers)s
    The full HTTP headers.

%(message)s
    The JSON response (the body).

Examples
========

- `HTTP Client using Requests
  <https://gist.github.com/bcb/cb0c90fa74e83bce616c>`_

`Back home <index.html>`_
