"""test_server.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main
import itertools
from collections import namedtuple

import requests
import responses

from jsonrpcclient import Server, rpc, exceptions


class TestServer(TestCase):

    def setUp(self):
        rpc.id_generator = itertools.count(1) # Ensure the first generated is 1
        self.server = Server('http://non-existant/')

    # Test instantiating

    @staticmethod
    def test_server_url_only():
        Server('http://example.com/api')

    @staticmethod
    def test_server_with_headers():
        Server('http://example.com/api', headers={'Content-Type': 'application/json-rpc'})

    @staticmethod
    def test_server_with_auth():
        Server('http://example.com/api', auth=('user', 'pass'))

    # Test the public methods (request and notify)

    @responses.activate
    def test_notify(self):
        responses.add(responses.POST, 'http://non-existant/', status=200)
        self.server.notify('go')

    @responses.activate
    def test_notify_alternate(self):
        responses.add(responses.POST, 'http://non-existant/', status=200)
        self.server.go()

    @responses.activate
    def test_request(self):
        responses.add(responses.POST, 'http://non-existant/', status=200, body='{"jsonrpc": "2.0", "result": 5, "id": null}')
        self.server.request('add', 1, 2)

    @responses.activate
    def test_request_alternate(self):
        responses.add(responses.POST, 'http://non-existant/', status=200, body='{"jsonrpc": "2.0", "result": 5, "id": null}')
        self.server.add(1, 2, response=True)

    # Test send_message()

    def test_send_message_with_connection_error(self):
        with self.assertRaises(exceptions.ConnectionError):
            self.server.send_message(rpc.request('go'))

    @responses.activate
    def test_send_message_with_invalid_request(self):
        # Impossible to pass an invalid dict, so just assume the exception was raised
        responses.add(responses.POST, 'http://non-existant/', status=400, body=requests.exceptions.InvalidSchema())
        with self.assertRaises(exceptions.InvalidRequest):
            self.server.send_message(rpc.request('go'))

    # Test handle_response()

    def test_handle_response_with_unwanted_text(self):
        response = namedtuple('Response', 'status_code, text')
        response.status_code = 200
        response.text = '{"jsonrpc": "2.0", "result": 5, "id": null}'
        with self.assertRaises(exceptions.UnwantedResponse):
            self.server.handle_response(response)

    def test_handle_response_with_no_text_but_expected_text(self):
        response = namedtuple('Response', 'status_code, text')
        response.status_code = 404
        response.text = ''
        with self.assertRaises(exceptions.ReceivedNoResponse):
            self.server.handle_response(response, expected_response=True)

    def test_handle_response_with_dodgy_text(self):
        response = namedtuple('Response', 'status_code, text')
        response.status_code = 200
        response.text = '{dodgy}'
        with self.assertRaises(exceptions.ParseResponseError):
            self.server.handle_response(response)

    def test_handle_response_with_non_validating_text(self):
        response = namedtuple('Response', 'status_code, text')
        response.status_code = 200
        response.text = '{"json": "2.0"}'
        with self.assertRaises(exceptions.InvalidResponse):
            self.server.handle_response(response, expected_response=True)

    def test_handle_response_with_error_text(self):
        response = namedtuple('Response', 'status_code, text')
        response.status_code = 404
        response.text = '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}, "id": null}'
        with self.assertRaises(exceptions.ReceivedErrorResponse):
            self.server.handle_response(response, expected_response=True)

    def test_handle_response_with_result_but_non_200_status(self):
        response = namedtuple('Response', 'status_code, text')
        response.status_code = 404
        response.text = '{"jsonrpc": "2.0", "result": 5, "id": null}'
        with self.assertRaises(exceptions.Non200Response):
            self.server.handle_response(response, expected_response=True)

    def test_handle_response_with_no_text_and_non_200_status(self):
        response = namedtuple('Response', 'status_code, text')
        response.status_code = 404
        response.text = ''
        with self.assertRaises(exceptions.Non200Response):
            self.server.handle_response(response)

if __name__ == '__main__':
    main()
