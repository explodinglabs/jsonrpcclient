"""test_http_server.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main
import itertools
from urllib.parse import urlencode

import requests
import responses

from jsonrpcclient import request
from jsonrpcclient.request import Request
from jsonrpcclient.http_server import HTTPServer


class TestHTTPServer(TestCase):

    def setUp(self):
        # Monkey patch id_iterator to ensure the request id is always 1
        request.id_iterator = itertools.count(1)

    @staticmethod
    def test_endpoint_only():
        HTTPServer('http://test/')

    def test_body(self):
        s = HTTPServer('http://test/')
        req = Request('go')
        try:
            s.send_message(req)
        except(requests.exceptions.RequestException):
            pass
        self.assertEqual(urlencode(req), s.last_request.body)

    def test_headers(self):
        s = HTTPServer('http://test/')
        req = Request('go')
        try:
            s.send_message(req)
        except(requests.exceptions.RequestException):
            pass
        self.assertEqual('application/json', s.last_request.headers['Content-Type'])
        self.assertEqual('application/json', s.last_request.headers['Accept'])
        self.assertIn('Content-Length', s.last_request.headers)

    def test_headers_set_in_init(self):
        s = HTTPServer('http://test/', headers={
            'Content-Type': 'application/json-rpc'})
        req = Request('go')
        try:
            s.send_message(req)
        except(requests.exceptions.RequestException):
            pass
        # Header set by argument
        self.assertEqual('application/json-rpc',
                s.last_request.headers['Content-Type'])
        # Header set by DEFAULT_HEADERS
        self.assertEqual('application/json',
                s.last_request.headers['Accept'])
        # Header set by Requests
        self.assertIn('Content-Length', s.last_request.headers)

    @staticmethod
    def test_with_auth():
        HTTPServer('http://test/', auth=('user', 'pass'))

    def test_send_message_with_connection_error(self):
        s = HTTPServer('http://test/')
        with self.assertRaises(requests.exceptions.RequestException):
            s.send_message(Request('go'))

    @responses.activate
    def test_send_message_with_invalid_request(self):
        s = HTTPServer('http://test/')
        # Impossible to pass an invalid dict, so just assume the exception was raised
        responses.add(responses.POST, 'http://test/', status=400, body=requests.exceptions.InvalidSchema())
        with self.assertRaises(requests.exceptions.InvalidSchema):
            s.send_message(Request('go'))

    @responses.activate
    def test_send_message_with_success_200(self):
        s = HTTPServer('http://test/')
        responses.add(responses.POST, 'http://test/', status=200, body='{"jsonrpc": "2.0", "result": 5, "id": 1}')
        s.send_message(Request('go'))


if __name__ == '__main__':
    main()
