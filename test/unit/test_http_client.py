"""test_http_client.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods,protected-access

from unittest import TestCase, main
import itertools
try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode

import requests
import responses

from jsonrpcclient import Request
from jsonrpcclient.http_client import HTTPClient


class TestHTTPClient(TestCase):

    def setUp(self):
        # Patch Request.id_iterator to ensure the id is always 1
        Request.id_iterator = itertools.count(1)

    @staticmethod
    def test_init_endpoint_only():
        HTTPClient('http://test/')

    def test_init_default_headers(self):
        s = HTTPClient('http://test/')
        # Default headers
        self.assertEqual('application/json', s.session.headers['Content-Type'])
        self.assertEqual('application/json', s.session.headers['Accept'])
        # Ensure the Requests default_headers are also there
        self.assertIn('Connection', s.session.headers)

    def test_init_custom_headers(self):
        s = HTTPClient('http://test/')
        s.session.headers['Content-Type'] = 'application/json-rpc'
        # Header set by argument
        self.assertEqual('application/json-rpc', s.session.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json', s.session.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Connection', s.session.headers)

    def test_init_custom_headers_are_sent(self):
        s = HTTPClient('http://test/')
        s.session.headers['Content-Type'] = 'application/json-rpc'
        req = Request('go')
        with self.assertRaises(requests.exceptions.RequestException):
            s._send_message(req)
        # Header set by argument
        self.assertEqual('application/json-rpc', s.last_request.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json', s.last_request.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Content-Length', s.last_request.headers)

    @staticmethod
    def test_init_custom_auth():
        HTTPClient('http://test/')

    # _send_message
    def test_send_message_body(self):
        s = HTTPClient('http://test/')
        req = Request('go')
        with self.assertRaises(requests.exceptions.RequestException):
            s._send_message(req)
        self.assertEqual(urlencode(req), s.last_request.body)

    def test_send_message_with_connection_error(self):
        s = HTTPClient('http://test/')
        with self.assertRaises(requests.exceptions.RequestException):
            s._send_message(Request('go'))

    @responses.activate
    def test_send_message_with_invalid_request(self):
        s = HTTPClient('http://test/')
        # Impossible to pass an invalid dict, so just assume the exception was raised
        responses.add(responses.POST, 'http://test/', status=400, body=requests.exceptions.InvalidSchema())
        with self.assertRaises(requests.exceptions.InvalidSchema):
            s._send_message(Request('go'))

    @staticmethod
    @responses.activate
    def test_send_message_with_success_200():
        s = HTTPClient('http://test/')
        responses.add(responses.POST, 'http://test/', status=200, body='{"jsonrpc": "2.0", "result": 5, "id": 1}')
        s._send_message(Request('go'))

    def test_send_message_custom_headers(self):
        s = HTTPClient('http://test/')
        req = Request('go')
        with self.assertRaises(requests.exceptions.RequestException):
            s._send_message(req, headers={'Content-Type': 'application/json-rpc'})
        # Header set by argument
        self.assertEqual('application/json-rpc', s.last_request.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json', s.last_request.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Content-Length', s.last_request.headers)

    def test_custom_headers_in_both_init_and_send_message(self):
        s = HTTPClient('http://test/')
        s.session.headers['Content-Type'] = 'application/json-rpc'
        req = Request('go')
        with self.assertRaises(requests.exceptions.RequestException):
            s._send_message(req, headers={'Accept': 'application/json-rpc'})
        # Header set by argument
        self.assertEqual('application/json-rpc', s.last_request.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json-rpc', s.last_request.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Content-Length', s.last_request.headers)

    def test_ssl_verification(self):
        s = HTTPClient('https://test/')
        s.session.cert = '/path/to/cert'
        s.session.verify = 'ca-cert'
        req = Request('go')
        with self.assertRaises(requests.exceptions.RequestException):
            s._send_message(req)


if __name__ == '__main__':
    main()
