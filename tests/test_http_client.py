"""test_http_client.py"""
from unittest import TestCase, main
import itertools

import requests
import responses

from jsonrpcclient.request import Request
from jsonrpcclient.prepared_request import PreparedRequest
from jsonrpcclient.http_client import HTTPClient


class TestHTTPClient(TestCase):
    def setUp(self):
        # Patch Request.id_iterator to ensure the id is always 1
        Request.id_iterator = itertools.count(1)

    @staticmethod
    def test_init_endpoint_only():
        HTTPClient('http://test/')

    def test_init_default_headers(self):
        client = HTTPClient('http://test/')
        # Default headers
        self.assertEqual('application/json', client.session.headers['Content-Type'])
        self.assertEqual('application/json', client.session.headers['Accept'])
        # Ensure the Requests default_headers are also there
        self.assertIn('Connection', client.session.headers)

    def test_init_custom_headers(self):
        client = HTTPClient('http://test/')
        client.session.headers['Content-Type'] = 'application/json-rpc'
        # Header set by argument
        self.assertEqual('application/json-rpc', client.session.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json', client.session.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Connection', client.session.headers)

    def test_send_custom_headers(self):
        client = HTTPClient('http://test/')
        client.session.headers['Content-Type'] = 'application/json-rpc'
        request = PreparedRequest(Request('go'))
        client._prepare_request(request)
        with self.assertRaises(requests.exceptions.RequestException):
            client._send_message(request)
        # Header set by argument
        self.assertEqual('application/json-rpc', request.prepped.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json', request.prepped.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Content-Length', request.prepped.headers)

    @staticmethod
    def test_init_custom_auth():
        HTTPClient('http://test/')

class TestHTTPClientSendMessage(TestCase):

    def setUp(self):
        # Patch Request.id_iterator to ensure the id is always 1
        Request.id_iterator = itertools.count(1)

    # _send_message
    def test_body(self):
        client = HTTPClient('http://test/')
        request = PreparedRequest(Request('go'))
        client._prepare_request(request)
        with self.assertRaises(requests.exceptions.RequestException):
            client._send_message(request)
        self.assertEqual(request, request.prepped.body)

    def test_connection_error(self):
        client = HTTPClient('http://test/')
        request = PreparedRequest(Request('go'))
        client._prepare_request(request)
        with self.assertRaises(requests.exceptions.RequestException):
            client._send_message(request)

    @responses.activate
    def test_invalid_request(self):
        client = HTTPClient('http://test/')
        request = PreparedRequest(Request('go'))
        client._prepare_request(request)
        # Impossible to pass an invalid dict, so just assume the exception was raised
        responses.add(
            responses.POST, 'http://test/', status=400,
            body=requests.exceptions.InvalidSchema())
        with self.assertRaises(requests.exceptions.InvalidSchema):
            client._send_message(request)

    @staticmethod
    @responses.activate
    def test_success_200():
        client = HTTPClient('http://test/')
        request = PreparedRequest(Request('go'))
        client._prepare_request(request)
        responses.add(
            responses.POST, 'http://test/', status=200,
            body='{"jsonrpc": "2.0", "result": 5, "id": 1}')
        client._send_message(request)

    def test_custom_headers(self):
        client = HTTPClient('http://test/')
        request = PreparedRequest(Request('go'))
        client._prepare_request(request, headers={'Content-Type': 'application/json-rpc'})
        with self.assertRaises(requests.exceptions.RequestException):
            client._send_message(request)
        # Header set by argument
        self.assertEqual('application/json-rpc', request.prepped.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json', request.prepped.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Content-Length', request.prepped.headers)

    def test_custom_headers_in_both(self):
        client = HTTPClient('http://test/')
        client.session.headers['Content-Type'] = 'application/json-rpc'
        request = PreparedRequest(Request('go'))
        client._prepare_request(request, headers={'Accept': 'application/json-rpc'})
        with self.assertRaises(requests.exceptions.RequestException):
            client._send_message(request)
        # Header set by argument
        self.assertEqual('application/json-rpc', request.prepped.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json-rpc', request.prepped.headers['Accept'])
        # Header set by Requests default_headers
        self.assertIn('Content-Length', request.prepped.headers)

    def test_ssl_verification(self):
        client = HTTPClient('https://test/')
        client.session.cert = '/path/to/cert'
        client.session.verify = 'ca-cert'
        request = PreparedRequest(Request('go'))
        client._prepare_request(request)
        with self.assertRaises(requests.exceptions.RequestException):
            client._send_message(request)


if __name__ == '__main__':
    main()
