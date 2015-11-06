"""test_server.py"""
# pylint: disable=missing-docstring,line-too-long

from unittest import TestCase, main
import itertools
import json

from jsonschema import ValidationError
from testfixtures import LogCapture

from jsonrpcclient import Request, exceptions
from jsonrpcclient.server import Server


class DummyServer(Server):
    """A dummy class for testing the abstract Server class"""
    def send_message(self, request):
        return '{"jsonrpc": "2.0", "result": 15, "id": 1}'


class TestServer(TestCase):

    def setUp(self):
        Request.id_iterator = itertools.count(1)
        self.server = DummyServer('http://non-existant:80/')


class TestLogging(TestServer):

    def test_request(self):
        with LogCapture() as l:
            self.server.log_request('{"jsonrpc": "2.0", "method": "go"}')
        l.check(('jsonrpcclient.server.request', 'INFO', '{"jsonrpc": "2.0", "method": "go"}'))

    def test_response(self):
        with LogCapture() as l:
            self.server.log_response('{"jsonrpc": "2.0", "result": 5, "id": 1}')
        l.check(('jsonrpcclient.server.response', 'INFO', '{"jsonrpc": "2.0", "result": 5, "id": 1}'))


class TestSend(TestServer):

    def test(self):
        self.assertEqual(15, self.server.send({'jsonrpc': '2.0', 'method': 'out', 'id': 1}))


class TestRequest(TestServer):

    def test(self):
        self.assertEqual(15, self.server.request('multiply', 3, 5))


class TestNotify(TestServer):

    def test(self):
        self.assertEqual(15, self.server.notify('multiply', 3, 5))


class TestDirect(TestServer):

    def test_alternate_usage(self):
        self.assertEqual(15, self.server.multiply(3, 5))


class TestProcessResponse(TestServer):

    def test_none(self):
        response = None
        self.assertEqual(None, self.server._process_response(response))

    def test_empty_string(self):
        response = ''
        self.assertEqual(None, self.server._process_response(response))

    def test_valid_json(self):
        response = {'jsonrpc': '2.0', 'result': 5, 'id': 1}
        self.assertEqual(5, self.server._process_response(response))

    def test_valid_json_null_id(self):
        response = {'jsonrpc': '2.0', 'result': 5, 'id': None}
        self.assertEqual(5, self.server._process_response(response))

    def test_valid_string(self):
        response = '{"jsonrpc": "2.0", "result": 5, "id": 1}'
        self.assertEqual(5, self.server._process_response(response))

    def test_invalid_json(self):
        response = '{dodgy}'
        with self.assertRaises(exceptions.ParseResponseError):
            self.server._process_response(response)

    def test_invalid_jsonrpc(self):
        response = {'json': '2.0'}
        with self.assertRaises(ValidationError):
            self.server._process_response(response)

    def test_invalid_jsonrpc_no_validation(self):
        Server.validator = None
        response = {'json': '2.0'}
        self.server._process_response(response)

    def test_error_response(self):
        response = {'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'Not Found'}, 'id': None}
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server._process_response(response)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, None)

    def test_error_response_with_data(self):
        response = {'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'Not Found', 'data': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'}, 'id': None}
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server._process_response(response)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit')

    def test_batch(self):
        response = [
            {'jsonrpc': '2.0', 'result': 5, 'id': 1},
            {'jsonrpc': '2.0', 'result': None, 'id': 2},
            {'jsonrpc': '2.0', 'error': {'code': -32000, 'message': 'Not Found'}, 'id': 3}]
        self.assertEqual(response, self.server._process_response(response))

    def test_batch_string(self):
        response = '[ \
            {"jsonrpc": "2.0", "result": 5, "id": 1}, \
            {"jsonrpc": "2.0", "result": null, "id": 2}, \
            {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}, "id": 3}]'
        self.assertEqual(json.loads(response), self.server._process_response(response))


if __name__ == '__main__':
    main()
