# pylint: disable=missing-docstring,line-too-long,no-self-use
"""proxy_test.py"""

import unittest
import itertools
from nose.tools import assert_raises # pylint: disable=no-name-in-module

from .proxy import Proxy
from . import rpc
from . import exceptions

class ProxyTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods

    def setUp(self):
        rpc.id_generator = itertools.count(1) # First generated is 1

    def test_request(self):
        proxy = Proxy('http://non-existant/')
        with assert_raises(exceptions.ConnectionError):
            proxy.request('add', 1, 2)

    def test_notify(self):
        proxy = Proxy('http://non-existant/')
        with assert_raises(exceptions.ConnectionError):
            proxy.notify('add', 1, 2)

    def test_magic(self):
        proxy = Proxy('http://non-existant/')
        with assert_raises(exceptions.ConnectionError):
            proxy.add(1, 2)

    def test_handle_response_none(self):
        with assert_raises(exceptions.ParseError):
            Proxy.handle_response('{')
