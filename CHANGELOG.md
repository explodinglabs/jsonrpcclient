# jsonrpcclient Change Log

## 3.0.0 (Coming soon, now in master branch)

_The 3.x releases will support Python 3.5+ only._

- Remove the config module. Add new params to configure the client. (#46)
- Remove the `*_server.py` files, which were deprecated. (#79)
- Rename aiohttpClient to AiohttpClient.
- Include http status code and reason in aiohttp log entries.
- Remove headers from http_client's log entries, they weren't used.
- Update the Tornado client to subclass AsyncClient. (#44)
- Remove HTTPClient.last_request and last_response, they weren't used. (#27)
- Remove ReceivedErrorResponse.
- HTTP clients raise an exception on non-2xx status code response. (#67)
- Remove zmq_client module, use zeromq_client instead. (#84)
- Move all client modules into a `clients` subpackage. Import from
  jsonrpcclient.clients. (#83)
- Change code to python 3 style: remove future and past.builtins. Change super
  calls to just super(). Change basestring to str. (#71)
- Remove jsonrpcclient.Request and Notification. Import
  jsonrpcclient.request.Request and Notification instead.
- Remove jsonrpcclient.request. Import jsonrpcclient.clients.http_client.request instead.
- Remove the need for requests library to be installed, if not using it. (#85)
- Add type hints (#92)
- Log to the debug log level (not info).
- Add support configuration files.
- Remove the convenience functions (request and notify).
- Remove zeromq-async client.
- Configure logging pythonically.

## 2.6.0 (Jun 13, 2018)
- Add command-line interface, see `jsonrpc --help` (#62)
- Fix configuring requests lib (#65)

## 2.5.2 (Nov 29, 2017)
- Ignore empty error bodies

## 2.5.1 (Sep 4, 2017)
- Fix non-string exception 'data' value

## 2.5.0 (Aug 8, 2017)
- Add convenience functions 'request' and 'notify' (#54)

## 2.4.3 (Aug 8, 2017)
- Fix custom headers in Tornado Client (#52)

## 2.4.2 (Oct 12, 2016)
- Allow passing a list of strings to send()

## 2.4.1 (Oct 6, 2016)
- Fix response log prefix

## 2.4.0 (Oct 5, 2016)
- Add asychronous Zeromq client, see [blog post](https://bcb.github.io/jsonrpc/zeromq-async)

## 2.3.0 (Sep 28, 2016)
- Support websockets and aiohttp

## 2.2.4 (Sep 19, 2016)
- Internal refactoring, to make it easier to add clients.

## 2.2.3 (Sep 13, 2016)
- Rename "server" modules and classes to "client". The old names are
  deprecated.

## 2.2.2 (Sep 12, 2016)
- Don't disable log propagate

## 2.2.1 (Sep 12, 2016)
- Bugfix logging configuration

## 2.2.0 (Sep 12, 2016)
- Support Tornado adapter
- Improve logging configuration
