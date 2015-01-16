Release History
---------------

1.1.1 (2015-01-16)
^^^^^^^^^^^^^^^^^^

- More features available when communicating with the server, such as setting a
  timeout on requests, ssl verification, cookies etc.

- Now compatible with older Python versions (tested with 2.7.9).

1.1.0 (2014-12-30)
^^^^^^^^^^^^^^^^^^

- Out of beta. Some minor internal adjustments.

1.0.12 (2014-12-16)
^^^^^^^^^^^^^^^^^^^

- Default HTTP headers changed to meet `this document
  <http://www.simple-is-better.org/json-rpc/transport_http.html#post-request>`_.
- Ability to customize the headers.
- Logging has changed. See `Logging
  <https://jsonrpcclient.readthedocs.org/#logging>`_.

1.0.11 (2014-12-12)
^^^^^^^^^^^^^^^^^^^

- Rewrote an internal function, ``rpc.request``.

1.0.10 (2014-12-11)
^^^^^^^^^^^^^^^^^^^

- Exceptions have been cleaned up. The base exception is now named
  ``JsonRpcClientError``.
- Tests added for 100% code coverage.

1.0.9 (2014-12-02)
^^^^^^^^^^^^^^^^^^^

- Added authentication.
- Messages are now output on the INFO log level.
