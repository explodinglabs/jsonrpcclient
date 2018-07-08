# jsonrpcclient Change Log

## 3.0.0 (Jul 8, 2018)
This version supports Python 3.5+ only. Users of Python versions below 3.5
should continue to use the 2.x releases.

Changes:

- No longer importing Request and Notification in jsonrpcclient.__init__.
  Import them from the module, jsonrpcclient.request.
- Change code python 3 style, remove future and past.builtins. Change super
  calls to just super(). Change basestring to str. (#71)
- Move all client modules into a `clients` subpackage. Import from
  jsonrpcclient.clients. (#83)
- Remove zmq_client module, use zeromq_client instead. (#84)
- HTTP clients raise an exception on non-2xx status code response. (#67)
- Rename ReceivedErrorResponse to RecievedErrorResponseError. (#82)
- Remove HTTPClient.last_request and last_response, they weren't used. (#27)
- Update the Tornado client to subclass AsyncClient. (#44)
- Remove headers from http_client's log entries, they weren't used.
- Include http status code and reason in aiohttp log entries.
- Rename aiohttpClient to AiohttpClient.
- Remove the `*_server.py` files, which were deprecated. (#79)
- Remove the config module. Add new params to configure the client. (#46)

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
