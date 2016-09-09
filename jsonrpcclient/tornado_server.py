'''
TornadoServer
*************

Represents an endpoint to communicate with using Tornado asynchronous HTTP
client::

    from tornado import gen, ioloop

    @gen.coroutine
    def test():
        proxy = TornadoServer('http://example.com/api')
        result = yield proxy.some_method(42)
        print(result)

    ioloop.IOLoop.instance().run_sync(test)

'''

from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado.concurrent import Future

from .server import Server


class TornadoServer(Server):
    '''
    :param endpoint: The server address.
    :param async_http_client_class: Tornado asynchronous HTTP client class.
    :param kwargs: Keyword arguments to pass to the client initialiser.
    '''

    _default_headers = {
        'Content-Type' : 'application/json',
        'Accept'       : 'application/json'
    }


    def __init__(self, endpoint, async_http_client_class=AsyncHTTPClient, \
            **kwargs):
        super(TornadoServer, self).__init__(endpoint)

        self.http_client = async_http_client_class(**kwargs)

    def _process_response(self, response_future):
        future = Future()

        def process_response_callback(response_future):
            try:
                response = response_future.result()
                result = super(TornadoServer, self)._process_response(
                    response.body.decode())
            except Exception as ex: # pylint: disable=broad-except
                future.set_exception(ex)
            else:
                future.set_result(result)

        response_future.add_done_callback(process_response_callback)

        return future

    def _log_response_callback(self, future):
        ex = future.exception()
        if ex:
            if isinstance(ex, HTTPError):
                body = ex.response.body.decode() \
                    if ex.response and ex.response.body else None
                self._log_response(body, {
                    'http_code'    : ex.code,
                    'http_reason'  : ex.message,
                })
        else:
            response = future.result()
            self._log_response(response.body.decode(), {
                'http_code'    : response.code,
                'http_reason'  : response.reason,
                'http_headers' : response.headers
            })

    def _send_message(self, request, **kwargs):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :param kwargs: Keyword arguments to the Tornado request.
        :return: The response (a string for requests, None for notifications).
        """

        self._log_request(request)

        headers = dict(self._default_headers)
        headers.update(kwargs.get('headers', {}))

        future = self.http_client.fetch(self.endpoint, method='POST', \
            body=request, headers=headers, **kwargs)

        future.add_done_callback(self._log_response_callback)

        return future
