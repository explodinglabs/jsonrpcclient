.. rubric:: :doc:`index`

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

    In addition to headers and authentication, other arguments can allow you to
    set the timeout, cookies, SSL verification and more. For the full list of
    options see the request method `here
    <https://github.com/kennethreitz/requests/blob/master/requests/api.py>`__.

Exceptions
==========

:requests.exceptions.RequestException:
    If there was a problem transferring the message.

.. include:: _includes/exceptions.rst

.. <http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>`_

Logging
=======

.. include:: _includes/logging.rst

The request format has these fields:

:endpoint: The server endpoint, eg. ``http://example.com/api``.
:http_headers: The full HTTP headers.
:message: The JSON request (the body).

The response format has these fields:

:endpoint: The server endpoint, eg. ``http://example.com/api``.
:http_code: The HTTP status code received from the server, eg. ``400``.
:http_reason: The description of the status code, eg. ``BAD REQUEST``.
:http_headers: The full HTTP headers.
:message: The JSON response (the body).

Examples
========

- `HTTP Client using Requests
  <https://gist.github.com/bcb/cb0c90fa74e83bce616c>`_

:doc:`Back home <index>`
