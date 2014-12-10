"""exceptions_test.py"""
# pylint: disable=missing-docstring,line-too-long

import unittest

from jsonrpcclient import exceptions


class TestExceptions(unittest.TestCase): # pylint: disable=too-many-public-methods

    def test_ConnectionError(self):
        with self.assertRaises(exceptions.ConnectionError):
            raise exceptions.ConnectionError

    def test_InvalidRequest(self):
        with self.assertRaises(exceptions.InvalidRequest):
            raise exceptions.InvalidRequest()

    def test_Non200Response(self):
        with self.assertRaises(exceptions.Non200Response):
            raise exceptions.Non200Response(404)

    def test_ParseResponseError(self):
        with self.assertRaises(exceptions.ParseResponseError):
            raise exceptions.ParseResponseError

    def test_InvalidResponse(self):
        with self.assertRaises(exceptions.InvalidResponse):
            raise exceptions.InvalidResponse

    def test_ReceivedNoResponse(self):
        with self.assertRaises(exceptions.ReceivedNoResponse):
            raise exceptions.ReceivedNoResponse

    def test_ReceivedErrorResponse(self):
        with self.assertRaises(exceptions.ReceivedErrorResponse):
            raise exceptions.ReceivedErrorResponse(1, 'Member not found')
