import itertools
import json
import pytest
from unittest.mock import patch

from testfixtures import LogCapture, StringComparison

from jsonrpcclient import exceptions
from jsonrpcclient.request import Request
from jsonrpcclient.response import Response
from jsonrpcclient.client import Client


class DummyClient(Client):
    """A dummy client for testing the abstract Client class"""

    def send_message(self, request):
        return Response('{"jsonrpc": "2.0", "result": 1, "id": 1}')


class TestLogRequest:
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
                StringComparison(r".*blahblahbl...ahblahblah.*"),
            )
        )

    def test_untrimmed(self):
        """Should not trim"""
        req = '{"jsonrpc": "2.0", "method": "go", "params": {"blah": "%s"}}' % (
            "blah" * 100,
        )
        with LogCapture() as capture:
            DummyClient("foo").log_request(req)
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                StringComparison(r".*" + "blah" * 100 + ".*"),
            )
        )


class TestLogResponse:
    def test(self):
        with LogCapture() as capture:
            DummyClient("foo").log_response(
                Response('{"jsonrpc": "2.0", "result": 5, "id": 1}')
            )
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
            DummyClient("foo").log_response(Response(req), trim=True)
        capture.check(
            (
                "jsonrpcclient.client.response",
                "INFO",
                StringComparison(r".*blahblahbl...ahblahblah.*"),
            )
        )

    def test_untrimmed(self):
        """Should not trim"""
        res = '{"jsonrpc": "2.0", "result": {"blah": "%s"}}' % ("blah" * 100,)
        with LogCapture() as capture:
            DummyClient("foo").log_response(Response(res))
        capture.check(
            (
                "jsonrpcclient.client.response",
                "INFO",
                StringComparison(r".*" + "blah" * 100 + ".*"),
            )
        )


class TestSend:
    @patch("jsonrpcclient.client.request_log")
    def test_json_encoded(self, *_):
        response = DummyClient("foo").send(
            '{"jsonrpc": "2.0", "method": "foo", "id": 1}'
        )
        assert response.data.result == 1

    @patch("jsonrpcclient.client.request_log")
    def test_json_decoded(self, *_):
        response = DummyClient("foo").send({"jsonrpc": "2.0", "method": "foo", "id": 1})
        assert response.data.result == 1


class TestRequest:
    @patch("jsonrpcclient.client.request_log")
    def test(self, *_):
        response = DummyClient("foo").request("multiply", 3, 5)
        assert response.data.ok == True


class TestNotify:
    @patch("jsonrpcclient.client.request_log")
    def test(self, *_):
        response = DummyClient("foo").notify("multiply", 3, 5)
        assert response.data.ok == True


class TestDirect:
    @patch("jsonrpcclient.client.request_log")
    def test_alternate_usage(self, *_):
        response = DummyClient("foo").multiply(3, 5)
        assert response.data.ok == True
