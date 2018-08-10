import itertools
import pytest
from unittest.mock import patch
from collections import namedtuple
from testfixtures import LogCapture, StringComparison

import requests
import responses

from jsonrpcclient import id_generators
from jsonrpcclient.exceptions import ReceivedNon2xxResponseError
from jsonrpcclient.request import Request
from jsonrpcclient.clients.http_client import HTTPClient, request, notify


class TestInit:
    def setup_method(self):
        # Patch Request.id_generator to ensure the id is always 1
        Request.id_generator = itertools.count(1)

    @staticmethod
    def test_init_endpoint_only():
        HTTPClient("http://test/")

    def test_init_default_headers(self):
        client = HTTPClient("http://test/")
        # Default headers
        assert client.session.headers["Content-Type"] == "application/json"
        assert client.session.headers["Accept"] == "application/json"
        # Ensure the Requests default_headers are also there
        assert "Connection" in client.session.headers

    def test_init_custom_headers(self):
        client = HTTPClient("http://test/")
        client.session.headers["Content-Type"] = "application/json-rpc"
        # Header set by argument
        assert client.session.headers["Content-Type"] == "application/json-rpc"
        # Header set by DEFAULT_HEADERS
        assert client.session.headers["Accept"] == "application/json"
        # Header set by Requests default_headers
        assert "Connection" in client.session.headers

    @staticmethod
    def test_init_custom_auth():
        HTTPClient("http://test/")


class TestSendMessage:
    def setup_method(self):
        # Patch Request.id_iterator to ensure the id is always 1
        Request.id_iterator = itertools.count(1)

    @responses.activate
    def test(self):
        responses.add(
            responses.POST,
            "http://foo",
            status=200,
            body='{"jsonrpc": "2.0", "result": 5, "id": 1}',
        )
        HTTPClient("http://foo").send_message(Request("foo"))

    @responses.activate
    def test_non_2xx_response_error(self):
        responses.add(responses.POST, "http://foo", status=400)
        with pytest.raises(ReceivedNon2xxResponseError):
            HTTPClient("http://foo").request("foo")

    def test_ssl_verification(self):
        client = HTTPClient("https://test/")
        client.session.cert = "/path/to/cert"
        client.session.verify = "ca-cert"
        with pytest.raises(OSError):  # Invalid certificate
            client.send_message(str(Request("foo")))


Resp = namedtuple("Response", ("text", "reason", "headers", "status_code"))


class TestRequest:
    """Testing the "request" convenience function"""

    @patch("jsonrpcclient.client.request_log")
    @patch(
        "jsonrpcclient.clients.http_client.Session.send",
        return_value=Resp(
            text='{"jsonrpc": "2.0", "result": "bar", "id": 1}',
            reason="foo",
            headers="foo",
            status_code=200,
        ),
    )
    def test(self, *_):
        response = request("http://foo", "foo")
        assert response.data.result == "bar"

    @patch("jsonrpcclient.client.response_log")
    @patch(
        "jsonrpcclient.clients.http_client.Session.send",
        return_value=Resp(
            text='{"jsonrpc": "2.0", "result": "bar", "id": 1}',
            reason="foo",
            headers="foo",
            status_code=200,
        ),
    )
    def test_trim_log_values(self, *_):
        with LogCapture() as capture:
            request(
                "http://foo",
                "foo",
                blah="blah" * 100,
                request_id=1,
                trim_log_values=True,
            )
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                '{"jsonrpc": "2.0", "method": "foo", "params": {"blah": "blahblahbl...ahblahblah"}, "id": 1}',
            )
        )

    @patch("jsonrpcclient.client.response_log")
    @patch(
        "jsonrpcclient.clients.http_client.Session.send",
        return_value=Resp(
            text='{"jsonrpc": "2.0", "result": true, "id": 1}',
            reason="foo",
            headers="foo",
            status_code=200,
        ),
    )
    def test_id_generator(self, *_):
        with LogCapture() as capture:
            result = request("http://foo", "foo", id_generator=id_generators.random())
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                StringComparison(
                    r'{"jsonrpc": "2.0", "method": "foo", "id": "[a-z0-9]{8}"'
                ),
            )
        )


class TestNotify:
    """Testing the "notify" convenience function"""

    @patch("jsonrpcclient.client.request_log")
    @patch(
        "jsonrpcclient.clients.http_client.Session.send",
        return_value=Resp(
            text='{"jsonrpc": "2.0", "result": "bar", "id": 1}',
            reason="foo",
            headers="foo",
            status_code=200,
        ),
    )
    def test(self, *_):
        response = notify("http://foo", "foo")
        assert response.data.result == "bar"

    @patch("jsonrpcclient.client.response_log")
    @patch(
        "jsonrpcclient.clients.http_client.Session.send",
        return_value=Resp(text="", reason="foo", headers="foo", status_code=200),
    )
    def test_trim_log_values(self, *_):
        with LogCapture() as capture:
            notify("http://foo", "foo", blah="blah" * 100, trim_log_values=True)
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                '{"jsonrpc": "2.0", "method": "foo", "params": {"blah": "blahblahbl...ahblahblah"}}',
            )
        )
