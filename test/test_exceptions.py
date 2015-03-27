"""test_exceptions.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main

from jsonrpcclient import exceptions


class TestExceptions(TestCase):

    def test_InvalidRequest(self):
        with self.assertRaises(exceptions.InvalidRequest):
            raise exceptions.InvalidRequest()

    def test_ConnectionError(self):
        with self.assertRaises(exceptions.ConnectionError):
            raise exceptions.ConnectionError

    def test_Non200Response(self):
        with self.assertRaises(exceptions.Non200Response):
            raise exceptions.Non200Response(404)

    def test_ReceivedNoResponse(self):
        with self.assertRaises(exceptions.ReceivedNoResponse):
            raise exceptions.ReceivedNoResponse

    def test_UnwantedResponse(self):
        with self.assertRaises(exceptions.UnwantedResponse):
            raise exceptions.UnwantedResponse

    def test_ParseResponseError(self):
        with self.assertRaises(exceptions.ParseResponseError):
            raise exceptions.ParseResponseError

    def test_InvalidResponse(self):
        with self.assertRaises(exceptions.InvalidResponse):
            raise exceptions.InvalidResponse

    def test_ReceivedErrorResponse(self):
        with self.assertRaises(exceptions.ReceivedErrorResponse):
            raise exceptions.ReceivedErrorResponse(1, 'Member not found')

if __name__ == '__main__':
    main()
