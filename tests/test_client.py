from unittest import TestCase
from unittest.mock import patch
import itertools
import json

from jsonschema import ValidationError
from testfixtures import LogCapture

from jsonrpcclient import Request, config, exceptions
from jsonrpcclient.client import Client


class DummyClient(Client):
    """A dummy class for testing the abstract Client class"""

    def send_message(self, request):
        return 15


class TestClient(TestCase):
    def setUp(self):
        Request.id_iterator = itertools.count(1)

    def tearDown(self):
        config.validate = True


class TestLogging(TestClient):
    def test_request(self, *_):
        client = DummyClient("foo")
        with LogCapture() as capture:
            client.log_request('{"jsonrpc": "2.0", "method": "go"}')
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                '{"jsonrpc": "2.0", "method": "go"}',
            )
        )

    def test_response(self):
        client = DummyClient("foo")
        with LogCapture() as capture:
            client.log_response('{"jsonrpc": "2.0", "result": 5, "id": 1}')
        capture.check(
            (
                "jsonrpcclient.client.response",
                "INFO",
                '{"jsonrpc": "2.0", "result": 5, "id": 1}',
            )
        )

    def test_request_trim(self):
        blahs = "blah" * 100
        client = DummyClient("foo")
        with LogCapture() as capture:
            client.log_request(
                '{"jsonrpc": "2.0", "method": "go", "params": {"blah": "%s"}}'
                % (blahs,),
                trim=True,
            )
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                '{"jsonrpc": "2.0", "method": "go", "params": {"blah": "blahblahbl...ahblahblah"}}',
            )
        )

    def test_response_trim(self):
        blahs = "blah" * 100
        client = DummyClient("foo")
        with LogCapture() as capture:
            client.log_response(
                '{"jsonrpc": "2.0", "result": "%s", "id": 1}' % (blahs,), trim=True
            )
        capture.check(
            (
                "jsonrpcclient.client.response",
                "INFO",
                '{"jsonrpc": "2.0", "result": "blahblahbl...ahblahblah", "id": 1}',
            )
        )

    def test_trim_message(self):
        import json
        from jsonrpcclient.log import trim_message

        # test string abbreviation
        message = trim_message("blah" * 100)
        self.assertIn("...", message)
        # test list abbreviation
        message = trim_message(json.dumps({"list": [0] * 100}))
        self.assertIn("...", message)
        # test nested abbreviation
        message = trim_message(
            json.dumps(
                {
                    "obj": {
                        "list": [0] * 100,
                        "string": "blah" * 100,
                        "obj2": {"string2": "blah" * 100},
                    }
                }
            )
        )
        self.assertIn("...", json.loads(message)["obj"]["obj2"]["string2"])


class TestSend(TestClient):
    @patch("jsonrpcclient.client.Client.request_log")
    def test(self, *_):
        result = DummyClient("foo").send({"jsonrpc": "2.0", "method": "out", "id": 1})
        self.assertEqual(result, 15)


class TestRequest(TestClient):
    @patch("jsonrpcclient.client.Client.request_log")
    def test(self, *_):
        result = DummyClient("foo").request("multiply", 3, 5)
        self.assertEqual(result, 15)


class TestNotify(TestClient):
    @patch("jsonrpcclient.client.Client.request_log")
    def test(self, *_):
        result = DummyClient("foo").notify("multiply", 3, 5)
        self.assertEqual(result, 15)


class TestDirect(TestClient):
    @patch("jsonrpcclient.client.Client.request_log")
    def test_alternate_usage(self, *_):
        result = DummyClient("foo").multiply(3, 5)
        self.assertEqual(result, 15)


class TestProcessResponse(TestClient):
    @patch("jsonrpcclient.client.Client.request_log")
    def test_none(self, *_):
        result = DummyClient("foo").process_response(None)
        self.assertEqual(result, None)

    def test_empty_string(self):
        result = DummyClient("foo").process_response("")
        self.assertEqual(result, None)

    @patch("jsonrpcclient.client.Client.response_log")
    def test_valid_json(self, *_):
        result = DummyClient("foo").process_response(
            {"jsonrpc": "2.0", "result": 5, "id": 1}
        )
        self.assertEqual(result, 5)

    @patch("jsonrpcclient.client.Client.response_log")
    def test_valid_json_null_id(self, *_):
        result = DummyClient("foo").process_response(
            {"jsonrpc": "2.0", "result": 5, "id": None}
        )
        self.assertEqual(result, 5)

    @patch("jsonrpcclient.client.Client.response_log")
    def test_valid_string(self, *_):
        result = DummyClient("foo").process_response(
            '{"jsonrpc": "2.0", "result": 5, "id": 1}'
        )
        self.assertEqual(result, 5)

    @patch("jsonrpcclient.client.Client.response_log")
    def test_invalid_json(self, *_):
        with self.assertRaises(exceptions.ParseResponseError):
            DummyClient("foo").process_response("{dodgy}")

    @patch("jsonrpcclient.client.Client.response_log")
    def test_invalid_jsonrpc(self, *_):
        with self.assertRaises(ValidationError):
            DummyClient("foo").process_response({"json": "2.0"})

    @patch("jsonrpcclient.client.Client.response_log")
    def test_without_validation(self, *_):
        config.validate = False
        # Should not raise exception
        DummyClient("foo").process_response({"json": "2.0"})

    @patch("jsonrpcclient.client.Client.response_log")
    def test_error_response(self, *_):
        response = {
            "jsonrpc": "2.0",
            "error": {"code": -32000, "message": "Not Found"},
            "id": None,
        }
        with self.assertRaises(exceptions.ReceivedErrorResponse) as ex:
            DummyClient("foo").process_response(response)
        self.assertEqual(ex.exception.code, -32000)
        self.assertEqual(ex.exception.message, "Not Found")
        self.assertEqual(ex.exception.data, None)

    @patch("jsonrpcclient.client.Client.response_log")
    def test_error_response_with_data(self, *_):
        response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32000,
                "message": "Not Found",
                "data": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            },
            "id": None,
        }
        with self.assertRaises(exceptions.ReceivedErrorResponse) as ex:
            DummyClient("foo").process_response(response)
        self.assertEqual(ex.exception.code, -32000)
        self.assertEqual(ex.exception.message, "Not Found")
        self.assertEqual(
            ex.exception.data, "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        )

    @patch("jsonrpcclient.client.Client.response_log")
    def test_error_response_with_nonstring_data(self, *_):
        """Reported in issue #56"""
        response = {
            "jsonrpc": "2.0",
            "error": {"code": -32000, "message": "Not Found", "data": {}},
            "id": None,
        }
        with self.assertRaises(exceptions.ReceivedErrorResponse) as ex:
            DummyClient("foo").process_response(response)
        self.assertEqual(ex.exception.code, -32000)
        self.assertEqual(ex.exception.message, "Not Found")
        self.assertEqual(ex.exception.data, {})

    @patch("jsonrpcclient.client.Client.response_log")
    def test_batch(self, *_):
        response = [
            {"jsonrpc": "2.0", "result": 5, "id": 1},
            {"jsonrpc": "2.0", "result": None, "id": 2},
            {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": "Not Found"},
                "id": 3,
            },
        ]
        result = DummyClient("foo").process_response(response)
        self.assertEqual(result, response)

    @patch("jsonrpcclient.client.Client.response_log")
    def test_batch_string(self, *_):
        response = (
            "["
            '{"jsonrpc": "2.0", "result": 5, "id": 1},'
            '{"jsonrpc": "2.0", "result": null, "id": 2},'
            '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}, "id": 3}]'
        )
        result = DummyClient("foo").process_response(response)
        self.assertEqual(result, json.loads(response))
