import itertools
import json
from unittest.mock import patch

import pytest
from testfixtures import LogCapture, StringComparison

from jsonrpcclient import exceptions
from jsonrpcclient.client import Client
from jsonrpcclient.request import Request
from jsonrpcclient.response import Response


class DummyClient(Client):
    """A dummy client for testing the abstract Client class"""

    def send_message(self, request):
        return Response('{"jsonrpc": "2.0", "result": 1, "id": 1}')


class TestLogRequest:
    def test(self, *_):
        with LogCapture() as capture:
            DummyClient().log_request('{"jsonrpc": "2.0", "method": "foo"}')
        capture.check(
            (
                "jsonrpcclient.client.request",
                "DEBUG",
                StringComparison(r'.*"method": "foo".*'),
            )
        )

    def test_trimmed(self):
        req = '{"jsonrpc": "2.0", "method": "go", "params": {"foo": "%s"}}' % (
            "foo" * 100,
        )
        with LogCapture() as capture:
            DummyClient().log_request(req, trim_log_values=True)
        capture.check(
            (
                "jsonrpcclient.client.request",
                "DEBUG",
                StringComparison(r".*foofoofoof...ofoofoofoo.*"),
            )
        )

    def test_untrimmed(self):
        """Should not trim"""
        req = '{"jsonrpc": "2.0", "method": "go", "params": {"foo": "%s"}}' % (
            "foo" * 100,
        )
        with LogCapture() as capture:
            DummyClient().log_request(req, trim_log_values=False)
        capture.check(
            (
                "jsonrpcclient.client.request",
                "DEBUG",
                StringComparison(r".*" + "foo" * 100 + ".*"),
            )
        )


class TestLogResponse:
    def test(self):
        with LogCapture() as capture:
            DummyClient().log_response(
                Response('{"jsonrpc": "2.0", "result": 5, "id": 1}')
            )
        capture.check(
            (
                "jsonrpcclient.client.response",
                "DEBUG",
                StringComparison(r'.*"result": 5.*'),
            )
        )

    def test_trimmed(self):
        req = '{"jsonrpc": "2.0", "result": "%s", "id": 1}' % ("foo" * 100,)
        with LogCapture() as capture:
            DummyClient().log_response(Response(req), trim_log_values=True)
        capture.check(
            (
                "jsonrpcclient.client.response",
                "DEBUG",
                StringComparison(r".*foofoofoof...ofoofoofoo.*"),
            )
        )

    def test_untrimmed(self):
        """Should not trim"""
        res = '{"jsonrpc": "2.0", "result": {"foo": "%s"}}' % ("foo" * 100,)
        with LogCapture() as capture:
            DummyClient().log_response(Response(res), trim_log_values=False)
        capture.check(
            (
                "jsonrpcclient.client.response",
                "DEBUG",
                StringComparison(r".*" + "foo" * 100 + ".*"),
            )
        )


class TestSending:
    @patch("jsonrpcclient.client.request_log")
    def test_send_string(self, *_):
        request = '{"jsonrpc": "2.0", "method": "foo", "id": 1}'
        response = DummyClient().send(request)
        assert response.data.ok == True
        assert response.data.result == 1

    @patch("jsonrpcclient.client.request_log")
    def test_send_dict(self, *_):
        request = {"jsonrpc": "2.0", "method": "foo", "id": 1}
        response = DummyClient().send(request)
        assert response.data.ok == True

    @patch("jsonrpcclient.client.request_log")
    def test_send_batch(self, *_):
        requests = [Request("foo"), Request("bar")]
        response = DummyClient().send(requests)
        assert response.data.ok == True

    @patch("jsonrpcclient.client.request_log")
    def test_request(self, *_):
        response = DummyClient().request("multiply", 3, 5)
        assert response.data.ok == True

    @patch("jsonrpcclient.client.request_log")
    def test_notify(self, *_):
        response = DummyClient().notify("multiply", 3, 5)
        assert response.data.ok == True

    @patch("jsonrpcclient.client.request_log")
    def test_alternate_usage(self, *_):
        response = DummyClient().multiply(3, 5)
        assert response.data.ok == True
