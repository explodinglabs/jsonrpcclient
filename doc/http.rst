jsonrpcclient over HTTP
***********************

Make JSON-RPC requests over HTTP.

Installation
============

.. code-block:: sh

    $ pip install jsonrpcclient requests

Usage
=====

Set the server details::

    >>> from jsonrpcclient.http_server import HTTPServer
    >>> server = HTTPServer('http://example.com/api')

.. include:: _includes/making_a_request.rst

Authentication
--------------

To make authenticated requests, pass an ``auth`` argument to ``HTTPServer``::

    >>> server = HTTPServer('http://example.com/api', auth=('user', 'pass'))

For more authentication options, see the `requests module
<http://docs.python-requests.org/en/latest/user/authentication/>`_ which
handles the authentication.

Headers
-------

To customize the HTTP headers, pass a ``headers`` argument to ``HTTPServer``::

    >>> server = HTTPServer('http://example.com/api', headers={'Content-Type': 'application/json-rpc'})

If no headers are given, the following headers are used::

    Content-Type: application/json
    Accept: application/json

.. note::

    In addition to ``auth`` and ``headers``, other arguments can allow you to
    set the timeout, cookies, ssl verification and more. For the full list of
    options see the request method `here
    <https://github.com/kennethreitz/requests/blob/master/requests/api.py>`_.

Exceptions
==========

In the event of a communications problem, the Requests module raises
`requests.exceptions.RequestException <http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions>`_::

    try:
        server.request('go')
    except requests.exceptions.RequestException as e:
        print(str(e))

Other standard exceptions are:

.. include:: _includes/standard_exceptions.rst

Logging
=======

.. include:: _includes/basic_logging.rst

For more advanced logging, use custom handlers and formats::

    import logging
    logging.getLogger('jsonrpcclient').setLevel(logging.INFO)

    request_handler = logging.StreamHandler()
    request_handler.setFormatter(logging.Formatter(fmt='%(endpoint)s --> %(message)s'))
    logging.getLogger('jsonrpcclient.server.request').addHandler(request_handler)

    response_handler = logging.StreamHandler()
    response_handler.setFormatter(logging.Formatter(fmt='%(endpoint)s <-- %(message)s'))
    logging.getLogger('jsonrpcclient.server.response').addHandler(response_handler)

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

- `JSON-RPC over HTTP Client in Python <https://bitbucket.org/snippets/beau-barker/KAjrB/json-rpc-over-http-client-in-python>`_

`Back home <index.html>`_
