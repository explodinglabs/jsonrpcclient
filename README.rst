jsonrpcclient
=============

Make `remote procedure calls
<http://en.wikipedia.org/wiki/Remote_procedure_call>`_ with `JSON-RPC
<http://www.jsonrpc.org/>`_.

..
    Using sourcode instead of code-block here due to bitbucket limitation.
    source-code:: works on both bitbucket and pypi.

.. sourcecode:: python

    >>> from jsonrpcclient import Server
    >>> server = Server('http://example.com/api')
    >>> server.request('add', 2, 3)
    5

* Documentation: http://jsonrpcclient.readthedocs.org/
* Package: https://pypi.python.org/pypi/jsonrpcclient
* Repository: https://bitbucket.org/beau-barker/jsonrpcclient
* Issue tracker: https://bitbucket.org/beau-barker/jsonrpcclient/issues

If you need a server, try my `jsonrpcserver
<https://pypi.python.org/pypi/jsonrpcserver>`_ library.
