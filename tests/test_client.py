import itertools
import json
import pytest
from unittest.mock import patch

from jsonschema import ValidationError
from testfixtures import LogCapture

from jsonrpcclient import exceptions
from jsonrpcclient.request import Request
from jsonrpcclient.client import Client


SENTINEL = object()


class DummyClient(Client):
    """A dummy client for testing the abstract Client class"""

    def send_message(self, request):
        return SENTINEL


class TestSend():
    @patch("jsonrpcclient.client.Client.request_log")
    def test(self, *_):
        result = DummyClient("foo").send({"jsonrpc": "2.0", "method": "out", "id": 1})
        assert result == SENTINEL

    def test_trim_log_values(self):
        req = '{"jsonrpc": "2.0", "method": "go", "params": {"blah": "%s"}}' % (
            "blah" * 100,
        )
        with LogCapture() as capture:
            DummyClient("foo", trim_log_values=True).send(req)
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                '{"jsonrpc": "2.0", "method": "go", "params": {"blah": "blahblahbl...ahblahblah"}}',
            )
        )


class TestRequest():
    @patch("jsonrpcclient.client.Client.request_log")
    def test(self, *_):
        result = DummyClient("foo").request("multiply", 3, 5)
        assert result == SENTINEL


class TestNotify():
    @patch("jsonrpcclient.client.Client.request_log")
    def test(self, *_):
        result = DummyClient("foo").notify("multiply", 3, 5)
        assert result == SENTINEL


class TestDirect():
    @patch("jsonrpcclient.client.Client.request_log")
    def test_alternate_usage(self, *_):
        result = DummyClient("foo").multiply(3, 5)
        assert result == SENTINEL


class TestProcessResponse():
    def setup_method(self):
        pass

    @patch("jsonrpcclient.client.Client.request_log")
    def test_none(self, *_):
        result = DummyClient("foo").process_response(None)
        assert result == None

    def test_empty_string(self):
        result = DummyClient("foo").process_response("")
        assert result == None

    @patch("jsonrpcclient.client.Client.response_log")
    def test_valid_json(self, *_):
        result = DummyClient("foo").process_response(
            {"jsonrpc": "2.0", "result": 5, "id": 1}
        )
        assert result == 5

    @patch("jsonrpcclient.client.Client.response_log")
    def test_valid_json_null_id(self, *_):
        result = DummyClient("foo").process_response(
            {"jsonrpc": "2.0", "result": 5, "id": None}
        )
        assert result == 5

    @patch("jsonrpcclient.client.Client.response_log")
    def test_valid_string(self, *_):
        result = DummyClient("foo").process_response(
            '{"jsonrpc": "2.0", "result": 5, "id": 1}'
        )
        assert result == 5

    @patch("jsonrpcclient.client.Client.response_log")
    def test_invalid_json(self, *_):
        with pytest.raises(exceptions.ParseResponseError):
            DummyClient("foo").process_response("{dodgy}")

    @patch("jsonrpcclient.client.Client.response_log")
    def test_invalid_jsonrpc(self, *_):
        with pytest.raises(ValidationError):
            DummyClient("foo").process_response({"json": "2.0"})

    @patch("jsonrpcclient.client.Client.response_log")
    def test_without_validation(self, *_):
        # Should not raise exception
        DummyClient("foo", validate_against_schema=False).process_response(
            {"json": "2.0"}
        )

    @patch("jsonrpcclient.client.Client.response_log")
    def test_error_response(self, *_):
        response = {
            "jsonrpc": "2.0",
            "error": {"code": -32000, "message": "Not Found"},
            "id": None,
        }
        with pytest.raises(exceptions.ReceivedErrorResponseError) as exc:
            DummyClient("foo").process_response(response)
        assert exc.value.code == -32000
        assert exc.value.message == "Not Found"
        assert exc.value.data == None

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
        with pytest.raises(exceptions.ReceivedErrorResponseError) as exc:
            DummyClient("foo").process_response(response)
        assert exc.value.code == -32000
        assert exc.value.message == "Not Found"
        assert exc.value.data == "Lorem ipsum dolor sit amet, consectetur adipiscing elit"

    @patch("jsonrpcclient.client.Client.response_log")
    def test_error_response_with_nonstring_data(self, *_):
        """Reported in issue #56"""
        response = {
            "jsonrpc": "2.0",
            "error": {"code": -32000, "message": "Not Found", "data": {}},
            "id": None,
        }
        with pytest.raises(exceptions.ReceivedErrorResponseError) as exc:
            DummyClient("foo").process_response(response)
        assert exc.value.code == -32000
        assert exc.value.message == "Not Found"
        assert exc.value.data == {}

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
        assert result == response

    @patch("jsonrpcclient.client.Client.response_log")
    def test_batch_string(self, *_):
        response = (
            "["
            '{"jsonrpc": "2.0", "result": 5, "id": 1},'
            '{"jsonrpc": "2.0", "result": null, "id": 2},'
            '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}, "id": 3}]'
        )
        result = DummyClient("foo").process_response(response)
        assert result == json.loads(response)


class TestLogRequest():
    def test(self, *_):
        with LogCapture() as capture:
            DummyClient("foo").log_request('{"jsonrpc": "2.0", "method": "go"}')
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                '{"jsonrpc": "2.0", "method": "go"}',
            )
        )

    def test_trimmed(self):
        req = '{"jsonrpc": "2.0", "method": "go", "params": {"blah": "%s"}}' % (
            "blah" * 100,
        )
        with LogCapture() as capture:
            DummyClient("foo").log_request(req, trim=True)
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                '{"jsonrpc": "2.0", "method": "go", "params": {"blah": "blahblahbl...ahblahblah"}}',
            )
        )


class TestLogResponse():
    def test(self):
        with LogCapture() as capture:
            DummyClient("foo").log_response('{"jsonrpc": "2.0", "result": 5, "id": 1}')
        capture.check(
            (
                "jsonrpcclient.client.response",
                "INFO",
                '{"jsonrpc": "2.0", "result": 5, "id": 1}',
            )
        )

    def test_trimmed(self):
        req = '{"jsonrpc": "2.0", "result": "%s", "id": 1}' % ("blah" * 100,)
        with LogCapture() as capture:
            DummyClient("foo").log_response(req, trim=True)
        capture.check(
            (
                "jsonrpcclient.client.response",
                "INFO",
                '{"jsonrpc": "2.0", "result": "blahblahbl...ahblahblah", "id": 1}',
            )
        )
