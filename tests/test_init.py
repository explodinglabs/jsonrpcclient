from unittest import TestCase
from unittest.mock import patch
from testfixtures import LogCapture, StringComparison
from collections import namedtuple

from jsonrpcclient import request, notify, ids


Resp = namedtuple("Response", ("text", "reason", "headers", "status_code"))


class TestRequest(TestCase):
    @patch("jsonrpcclient.client.Client.request_log")
    @patch("jsonrpcclient.HTTPClient.send_message", return_value="bar")
    def test(self, *_):
        result = request("http://foo", "foo")
        self.assertEqual(result, "bar")

    @patch("jsonrpcclient.client.Client.response_log")
    @patch(
        "jsonrpcclient.http_client.Session.send",
        return_value=Resp(
            text='{"jsonrpc": "2.0", "result": true, "id": 1}',
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

    @patch("jsonrpcclient.client.Client.response_log")
    @patch(
        "jsonrpcclient.http_client.Session.send",
        return_value=Resp(
            text='{"jsonrpc": "2.0", "result": true, "id": 1}',
            reason="foo",
            headers="foo",
            status_code=200,
        ),
    )
    def test_id_generator(self, *_):
        # Set id type in config to decimal
        import jsonrpcclient.config
        jsonrpcclient.config.ids = "decimal"
        with LogCapture() as capture:
            result = request("http://foo", "foo", id_generator=ids.random())
        capture.check(
            (
                "jsonrpcclient.client.request",
                "INFO",
                StringComparison(r'{"jsonrpc": "2.0", "method": "foo", "id": "[a-z0-9]{8}"')
            )
        )


class TestNotify(TestCase):
    @patch("jsonrpcclient.client.Client.request_log")
    @patch("jsonrpcclient.HTTPClient.send_message", return_value="bar")
    def test(self, *_):
        result = notify("http://foo", "foo")
        self.assertEqual(result, "bar")

    @patch("jsonrpcclient.client.Client.response_log")
    @patch(
        "jsonrpcclient.http_client.Session.send",
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
