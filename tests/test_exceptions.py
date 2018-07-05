from unittest import TestCase

from jsonrpcclient import exceptions


class TestExceptions(TestCase):
    def test_parse_response_error(self):
        with self.assertRaises(exceptions.ParseResponseError):
            raise exceptions.ParseResponseError

    def test_received_error_response(self):
        with self.assertRaises(exceptions.ReceivedErrorResponseError):
            raise exceptions.ReceivedErrorResponseError(1, "foo", "bar")

    def test_non_2xx_status_code_error(self):
        with self.assertRaises(exceptions.ReceivedNon2xxResponseError):
            raise exceptions.ReceivedNon2xxResponseError(404)
