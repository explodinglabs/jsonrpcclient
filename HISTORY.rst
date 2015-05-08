Release History
---------------

1.1.6 (2015-05-09)
^^^^^^^^^^^^^^^^^^

- Documentation changes.

1.1.5 (2015-05-09)
^^^^^^^^^^^^^^^^^^

- Removed Non2xxResponse error which served no real purpose.

1.1.4 (2015-05-09)
^^^^^^^^^^^^^^^^^^

- Non200Response error replaced with Non2xxResponse.
- Logging fixed - see the documentation for changes.

1.1.3 (2015-03-30)
^^^^^^^^^^^^^^^^^^

- Minor adjustments for compatibility with older Python versions.

1.1.2 (2015-02-06)
^^^^^^^^^^^^^^^^^^

- Bugfix - HTTP headers were often incorrect due to quirks in the requests
  module. Now using a different method to set the headers.

1.1.1 (2015-01-16)
^^^^^^^^^^^^^^^^^^

- More features available when communicating with the server, such as setting a
  timeout on requests, ssl verification, cookies etc.

- Now compatible with older Python versions.
