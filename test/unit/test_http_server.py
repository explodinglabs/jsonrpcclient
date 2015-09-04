"""test_http_server.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main
import itertools

import requests
import responses

from jsonrpcclient import rpc
from jsonrpcclient.rpc import rpc_request
from jsonrpcclient.http_server import HTTPServer


class TestHTTPServer(TestCase):

    def setUp(self):
        rpc.id_generator = itertools.count(1) # Ensure the first generated is 1
        self.server = HTTPServer('http://non-existant/')

    @staticmethod
    def test_http_server_endpoint_only():
        HTTPServer('http://example.com/api')

    @staticmethod
    def test_http_server_with_headers():
        HTTPServer('http://example.com/api', headers={'Content-Type': 'application/json-rpc'})

    @staticmethod
    def test_http_server_with_auth():
        HTTPServer('http://example.com/api', auth=('user', 'pass'))

    def test_send_message_with_connection_error(self):
        with self.assertRaises(requests.exceptions.RequestException):
            self.server.send_message(rpc_request('go'))

    @responses.activate
    def test_send_message_with_invalid_request(self):
        # Impossible to pass an invalid dict, so just assume the exception was raised
        responses.add(responses.POST, 'http://non-existant/', status=400, body=requests.exceptions.InvalidSchema())
        with self.assertRaises(requests.exceptions.InvalidSchema):
            self.server.send_message(rpc_request('go'))


if __name__ == '__main__':
    main()
