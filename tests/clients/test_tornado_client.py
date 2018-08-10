import json
import itertools
from unittest.mock import patch, Mock

from tornado import testing, web, httpclient

from jsonrpcclient.request import Request
from jsonrpcclient.exceptions import ReceivedNon2xxResponseError
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


class Test(testing.AsyncHTTPTestCase):
    def setup_method(self, *_):
        # Patch Request.id_generator to ensure the id is always 1
        Request.id_generator = itertools.count(1)

    def get_app(self):
        return web.Application([("/echo", EchoHandler), ("/fail", FailureHandler)])

    @patch("jsonrpcclient.client.request_log")
    @patch("jsonrpcclient.client.response_log")
    @testing.gen_test
    def test_request(self, *_):
        response = yield TornadoClient(self.get_url("/echo")).request(
            "foo", 1, [2], {"3": 4, "5": True, "6": None}
        )
        assert response.data.result == [1, [2], {"3": 4, "6": None, "5": True}]

    @patch("jsonrpcclient.client.request_log")
    @patch("jsonrpcclient.client.response_log")
    @testing.gen_test
    def test_custom_headers(self, *_):
        response = yield TornadoClient(self.get_url("/echo")).send(
            Request("foo", 1, [2], {"3": 4, "5": True, "6": None}),
            headers={"foo": "bar"},
        )
        assert response.data.result == [1, [2], {"3": 4, "6": None, "5": True}]
