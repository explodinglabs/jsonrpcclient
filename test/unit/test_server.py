"""test_server.py"""
# pylint: disable=missing-docstring,line-too-long

from unittest import TestCase, main
import itertools

from jsonschema import ValidationError
from testfixtures import LogCapture

from jsonrpcclient import rpc, exceptions
from jsonrpcclient.server import Server


class DummyServer(Server):
    """A dummy class for testing the abstract Server class"""
    def send_message(self, request):
        return '{"jsonrpc": "2.0", "result": 5, "id": 1}'


class TestServer(TestCase):

    def setUp(self):
        rpc.id_generator = itertools.count(1) # Ensure the first generated is 1
        self.server = DummyServer('http://non-existant:80/')


class TestLogging(TestServer):

    def test_log_request(self):
        with LogCapture() as l:
            self.server.log_request('{"jsonrpc": "2.0", "method": "go"}')
        l.check(('jsonrpcclient.server.request', 'INFO', '{"jsonrpc": "2.0", "method": "go"}'))

    def test_log_response(self):
        with LogCapture() as l:
            self.server.log_response('{"jsonrpc": "2.0", "result": 5, "id": 1}')
        l.check(('jsonrpcclient.server.response', 'INFO', '{"jsonrpc": "2.0", "result": 5, "id": 1}'))


class TestNotify(TestServer):

    def test_notify(self):
        self.server.notify('go')

    def test_notify_alternate_usage(self):
        self.server.go()


class TestRequest(TestServer):

    def test_request(self):
        self.assertEqual(5, self.server.request('add', 2, 3))

    def test_request_alternate_usage(self):
        self.assertEqual(5, self.server.add(2, 3, response=True))


class TestHandleResponseNotifications(TestServer):

    def test_handle_response_notification_with_no_response(self):
        response = None
        self.server._handle_response(response)

    def test_handle_response_notification_with_empty_string_response(self):
        response = ''
        self.server._handle_response(response)

    def test_handle_response_notification_with_invalid_json_response(self):
        response = '{dodgy}'
        with self.assertRaises(exceptions.ParseResponseError):
            self.server._handle_response(response)

    def test_handle_response_notification_with_invalid_jsonrpc_response(self):
        response = '{"json": "2.0"}'
        with self.assertRaises(ValidationError):
            self.server._handle_response(response)

    def test_handle_response_notification_with_valid_response(self):
        response = '{"jsonrpc": "2.0", "result": 5, "id": null}'
        self.server._handle_response(response)

    def test_handle_response_notification_with_error_response(self):
        response = '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found", "data": "A Primitive or Structured value that contains additional information about the error. This may be omitted. The value of this member is defined by the Server (e.g. detailed error information, nested errors etc.)"}, "id": null}'
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server._handle_response(response)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, 'A Primitive or Structured value that contains additional information about the error. This may be omitted. The value of this member is defined by the Server (e.g. detailed error information, nested errors etc.)')

    def test_handle_response_notification_with_error_without_data(self):
        response = '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}, "id": null}'
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server._handle_response(response)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, None)


class TestHandleResponseRequests(TestServer):

    def test_handle_response_request_with_no_response(self):
        response = None
        with self.assertRaises(exceptions.ReceivedNoResponse):
            self.server._handle_response(response, expected_response=True)

    def test_handle_response_request_with_empty_string_response(self):
        response = ''
        with self.assertRaises(exceptions.ReceivedNoResponse):
            self.server._handle_response(response, expected_response=True)

    def test_handle_response_request_with_invalid_json_response(self):
        response = '{dodgy}'
        with self.assertRaises(exceptions.ParseResponseError):
            self.server._handle_response(response, expected_response=True)

    def test_handle_response_request_with_invalid_jsonrpc_response(self):
        response = '{"json": "2.0"}'
        with self.assertRaises(ValidationError):
            self.server._handle_response(response, expected_response=True)

    def test_handle_response_request_with_valid_response(self):
        response = '{"jsonrpc": "2.0", "result": 5, "id": null}'
        self.assertEqual(5, self.server._handle_response(response, expected_response=True))

    def test_handle_response_request_with_error_response(self):
        response = '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found", "data": "A Primitive or Structured value that contains additional information about the error. This may be omitted. The value of this member is defined by the Server (e.g. detailed error information, nested errors etc.)"}, "id": null}'
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server._handle_response(response, expected_response=True)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, 'A Primitive or Structured value that contains additional information about the error. This may be omitted. The value of this member is defined by the Server (e.g. detailed error information, nested errors etc.)')

    def test_handle_response_request_with_error_without_data(self):
        response = '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}, "id": null}'
        with self.assertRaises(exceptions.ReceivedErrorResponse) as e:
            self.server._handle_response(response, expected_response=True)
        self.assertEqual(e.exception.code, -32000)
        self.assertEqual(e.exception.message, 'Not Found')
        self.assertEqual(e.exception.data, None)


if __name__ == '__main__':
    main()
