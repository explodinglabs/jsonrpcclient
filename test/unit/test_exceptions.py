"""test_exceptions.py"""
# pylint: disable=missing-docstring

from unittest import TestCase, main

from jsonrpcclient import exceptions


class TestExceptions(TestCase):

    def test_parse_response_error(self):
        with self.assertRaises(exceptions.ParseResponseError):
            raise exceptions.ParseResponseError

    def test_received_error_response(self):
        with self.assertRaises(exceptions.ReceivedErrorResponse):
            raise exceptions.ReceivedErrorResponse(1, 'foo', 'bar')


if __name__ == '__main__':
    main()
