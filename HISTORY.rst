Release History
---------------

1.0.12 (2014-12-16)
+++++++++++++++++++

- Default HTTP headers changed to meet `this document
  <http://www.simple-is-better.org/json-rpc/transport_http.html#post-request>`_.
- Ability to customize the headers.
- Logging has changed. See `Logging
  <http://jsonrpcclient.readthedocs.org/#logging>`_.

1.0.11 (2014-12-12)
+++++++++++++++++++

- Rewrote an internal function, ``rpc.request``.

1.0.10 (2014-12-11)
+++++++++++++++++++

- Exceptions have been cleaned up. The base exception is now named
  ``JsonRpcClientError``.
- Tests added for 100% code coverage.

1.0.9 (2014-12-02)
+++++++++++++++++++

- Added authentication.
- Messages are now output on the INFO log level.

1.0.8 (2014-12-02)
+++++++++++++++++++

- Show the response status code in the log.
