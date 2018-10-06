import itertools
from collections import namedtuple
from unittest.mock import patch

import pytest
import responses

from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.exceptions import ReceivedNon2xxResponseError
from jsonrpcclient.requests import Request


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
        HTTPClient("http://foo").send_message(
            str(Request("foo")), response_expected=True
        )

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
            client.send_message(str(Request("foo")), response_expected=True)


Resp = namedtuple("Response", ("text", "reason", "headers", "status_code"))


class TestRequest:
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
        response = HTTPClient("http://test/").request("http://foo", "foo")
        assert response.data.result == "bar"


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
        response = HTTPClient("http://test/").notify("http://foo", "foo")
        assert response.data.result == "bar"
