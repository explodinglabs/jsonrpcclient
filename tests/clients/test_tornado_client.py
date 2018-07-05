import json
import itertools
from unittest.mock import patch

from tornado import testing, web, httpclient

from jsonrpcclient import Request
from jsonrpcclient.clients.tornado_client import TornadoClient


class EchoHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        self.finish(
            {
                "id": 1,
                "jsonrpc": "2.0",
                "result": [1, [2], {"3": 4, "5": True, "6": None}],
            }
        )


class FailureHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        request = json.loads(self.request.body.decode())
        raise web.HTTPError(request["params"]["code"])


class TestTornadoClient(testing.AsyncHTTPTestCase):
    def get_app(self):
        return web.Application([("/echo", EchoHandler), ("/fail", FailureHandler)])

    def setUp(self):
        super(TestTornadoClient, self).setUp()
        # Patch Request.id_generator to ensure the id is always 1
        Request.id_generator = itertools.count(1)

    @patch("jsonrpcclient.client.Client.request_log")
    @patch("jsonrpcclient.client.Client.response_log")
    @testing.gen_test
    def test_success(self, *_):
        client = TornadoClient(self.get_url("/echo"))
        response = yield client.some_method(1, [2], {"3": 4, "5": True, "6": None})
        self.assertEqual([1, [2], {"3": 4, "6": None, "5": True}], response)

    @patch("jsonrpcclient.client.Client.request_log")
    @testing.gen_test
    def test_failure(self, *_):
        client = TornadoClient(self.get_url("/fail"))
        with self.assertRaises(httpclient.HTTPError) as ctx:
            yield client.fail(code=500)
        self.assertEqual("HTTP 500: Internal Server Error", str(ctx.exception))

    @patch("jsonrpcclient.client.Client.request_log")
    @patch("jsonrpcclient.client.Client.response_log")
    @testing.gen_test
    def test_custom_headers(self, *_):
        client = TornadoClient(self.get_url("/echo"))
        response = yield client.send(
            Request("some_method", 1, [2], {"3": 4, "5": True, "6": None}),
            headers={"foo": "bar"},
        )
        self.assertEqual([1, [2], {"3": 4, "6": None, "5": True}], response)
