"""test_http_server.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main
import itertools

import requests
import responses

from jsonrpcclient import request
from jsonrpcclient.request import rpc_request
from jsonrpcclient.http_server import HTTPServer


class TestHTTPServer(TestCase):

    def setUp(self):
        # Monkey patch id_iterator to ensure the request id is always 1
        request.id_iterator = itertools.count(1)
        self.server = HTTPServer('http://test/')

    @staticmethod
    def test_http_server_endpoint_only():
        HTTPServer('http://test/')

    @staticmethod
    def test_http_server_with_headers():
        HTTPServer('http://test/', headers={'Content-Type': 'application/json-rpc'})

    @staticmethod
    def test_http_server_with_auth():
        HTTPServer('http://test/', auth=('user', 'pass'))

    def test_send_message_with_connection_error(self):
        with self.assertRaises(requests.exceptions.RequestException):
            self.server.send_message(rpc_request('go'))

    @responses.activate
    def test_send_message_with_invalid_request(self):
        # Impossible to pass an invalid dict, so just assume the exception was raised
        responses.add(responses.POST, 'http://test/', status=400, body=requests.exceptions.InvalidSchema())
        with self.assertRaises(requests.exceptions.InvalidSchema):
            self.server.send_message(rpc_request('go'))

    @responses.activate
    def test_send_message_with_success_200(self):
        responses.add(responses.POST, 'http://test/', status=200, body='{"jsonrpc": "2.0", "result": 5, "id": 1}')
        self.server.send_message(rpc_request('go'))


if __name__ == '__main__':
    main()
