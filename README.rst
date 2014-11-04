.. -*-restructuredtext-*-

rpcclient
=========

A JSON-RPC 2.0 client library for Python.

.. sourcecode:: python
    >> import rpcclient
    >> proxy = rpcclient.Proxy('http://rpcserver/')
    >> proxy.add(1, 2)
    3
