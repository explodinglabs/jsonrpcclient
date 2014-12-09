"""exceptions_test.py"""
# pylint: disable=missing-docstring,line-too-long

import unittest

from jsonrpcclient import exceptions


class TestExceptions(unittest.TestCase): # pylint: disable=too-many-public-methods

    def test_ConnectionError(self):
        with self.assertRaises(exceptions.ConnectionError):
            raise exceptions.ConnectionError

    def test_StatusCodeError(self):
        with self.assertRaises(exceptions.StatusCodeError):
            raise exceptions.StatusCodeError(404)

    def test_ParseError(self):
        with self.assertRaises(exceptions.ParseError):
            raise exceptions.ParseError

    def test_InvalidResponse(self):
        with self.assertRaises(exceptions.InvalidResponse):
            raise exceptions.InvalidResponse

    def test_ReceivedNoResponse(self):
        with self.assertRaises(exceptions.ReceivedNoResponse):
            raise exceptions.ReceivedNoResponse

    def test_ReceivedErrorResponse(self):
        with self.assertRaises(exceptions.ReceivedErrorResponse):
            raise exceptions.ReceivedErrorResponse(1, 'Member not found')
