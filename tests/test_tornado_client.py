"""Tornado client test case"""
import json
import itertools

from tornado import testing, web, httpclient

from jsonrpcclient import Request
from jsonrpcclient.tornado_client import TornadoClient


class EchoHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        self.finish({
            'id'      : 1,
            'jsonrpc' : '2.0',
            'result'  : [1, [2], {'3': 4, '5': True, '6': None}]
        })


class FailureHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        request = json.loads(self.request.body.decode())
        raise web.HTTPError(request['params']['code'])


class TestTornadoClient(testing.AsyncHTTPTestCase):
    def get_app(self):
        return web.Application([
            ('/echo', EchoHandler),
            ('/fail', FailureHandler),
        ])

    def setUp(self):
        super(TestTornadoClient, self).setUp()
        # Patch Request.id_iterator to ensure the id is always 1
        Request.id_iterator = itertools.count(1)

    @testing.gen_test
    def test_success(self):
        testee = TornadoClient(self.get_url('/echo'))
        response = yield testee.some_method(1, [2], {'3': 4, '5': True, '6': None})
        self.assertEqual([1, [2], {'3': 4, '6': None, '5': True}], response)

    @testing.gen_test
    def test_failure(self):
        testee = TornadoClient(self.get_url('/fail'))
        with self.assertRaises(httpclient.HTTPError) as ctx:
            yield testee.fail(code=500)
        self.assertEqual('HTTP 500: Internal Server Error', str(ctx.exception))

    @testing.gen_test
    def test_custom_headers(self):
        testee = TornadoClient(self.get_url('/echo'))
        response = yield testee.send(
            Request('some_method', 1, [2], {'3': 4, '5': True, '6': None}),
            headers={'foo': 'bar'})
        self.assertEqual([1, [2], {'3': 4, '6': None, '5': True}], response)
