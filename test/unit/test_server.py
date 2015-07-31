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
        response = '{"jsonrpc": "2.0", "result": 5, "id": null}'
        with self.assertRaises(exceptions.UnwantedResponse):
            self.server.handle_response(response)

    def test_handle_response_with_no_text_but_expected_text(self):
        response = ''
        with self.assertRaises(exceptions.ReceivedNoResponse):
            self.server.handle_response('', expected_response=True)

    def test_handle_response_with_dodgy_text(self):
        response = '{dodgy}'
        with self.assertRaises(exceptions.ParseResponseError):
            self.server.handle_response(response)

    def test_handle_response_with_non_validating_text(self):
        response = '{"json": "2.0"}'
        with self.assertRaises(exceptions.InvalidResponse):
            self.server.handle_response(response, expected_response=True)

    def test_handle_error_response(self):
        response = '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found", "data": "A Primitive or Structured value that contains additional information about the error. This may be omitted. The value of this member is defined by the Server (e.g. detailed error information, nested errors etc.)"}, "id": null}'
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server.handle_response(response, expected_response=True)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, 'A Primitive or Structured value that contains additional information about the error. This may be omitted. The value of this member is defined by the Server (e.g. detailed error information, nested errors etc.)')

    def test_handle_error_response_without_data(self):
        response = '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}, "id": null}'
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server.handle_response(response, expected_response=True)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, None)

if __name__ == '__main__':
    main()
