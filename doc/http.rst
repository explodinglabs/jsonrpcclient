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

Configuration
=============

The `requests.Session
<http://docs.python-requests.org/en/master/api/#requests.Session>`_ is
available so you can configure the Requests module.

For example, for basic auth::

    >>> server.session.auth = ('user', 'pass')

SSL authentication::

    >>> server.session.verify = '/path/to/cert'

Customize the HTTP headers::

    >>> server.session.headers.update({'Content-Type': 'application/json-rpc'})

You can also configure the `Request
<http://docs.python-requests.org/en/master/api/#requests.Request>`_ options
when calling ``send``::

    >>> server.send(req, auth=('user', 'pass'))
    >>> server.send(req, headers={'Content-Type': 'application/json-rpc'})

Any dictionaries passed to ``send`` in named arguments will be merged with the
session-level values that are set. The method-level parameters override session
parameters.

Exceptions
==========

:requests.exceptions.RequestException:
    If there was a problem transferring the message.

.. include:: _includes/exceptions.rst

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
