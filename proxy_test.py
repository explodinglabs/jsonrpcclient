"""proxy_test.py"""
# pylint: disable=missing-docstring,line-too-long

from nose.tools import assert_raises # pylint: disable=no-name-in-module

from .proxy import Proxy
from . import exceptions

def test_ConnectionError():
    proxy = Proxy('http://non-existant.com.au/')
    with assert_raises(exceptions.ConnectionError):
        proxy.add(1, 2)
