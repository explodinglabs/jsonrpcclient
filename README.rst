.. -*-restructuredtext-*-

rpcclient
=========

A JSON-RPC 2.0 client library for Python.

.. sourcecode:: python
    >> import rpcclient
    >> proxy = rpcclient.Proxy('http://127.0.0.1/:5000')
    >> proxy.add(1, 2)
    3
