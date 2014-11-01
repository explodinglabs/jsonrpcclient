"""exceptions_test.py"""
# pylint: disable=missing-docstring,line-too-long

from nose.tools import assert_raises # pylint: disable=no-name-in-module

from . import exceptions

def test_ConnectionError():
    with assert_raises(exceptions.ConnectionError):
        raise exceptions.ConnectionError

def test_StatusCodeError():
    with assert_raises(exceptions.StatusCodeError):
        raise exceptions.StatusCodeError(404)

def test_ParseError():
    with assert_raises(exceptions.ParseError):
        raise exceptions.ParseError

def test_InvalidResponse():
    with assert_raises(exceptions.InvalidResponse):
        raise exceptions.InvalidResponse

def test_ReceivedNoResponse():
    with assert_raises(exceptions.ReceivedNoResponse):
        raise exceptions.ReceivedNoResponse

def test_ReceivedErrorResponse():
    with assert_raises(exceptions.ReceivedErrorResponse):
        raise exceptions.ReceivedErrorResponse(1, 'Member not found')
