# pylint: disable=missing-docstring,line-too-long,no-self-use
"""server_test.py"""

import unittest
import itertools
import logging

from nose.tools import assert_raises # pylint: disable=no-name-in-module

from jsonrpcclient.server import Server
from jsonrpcclient import rpc
from jsonrpcclient import exceptions

class ServerTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods

    def setUp(self):
        rpc.id_generator = itertools.count(1) # First generated is 1
        self.server = Server('http://non-existant/')

    def test_request(self):
        with assert_raises(exceptions.ConnectionError):
            self.server.request('add', 1, 2)

    def test_notify(self):
        with assert_raises(exceptions.ConnectionError):
            self.server.notify('add', 1, 2)

    def test_magic(self):
        with assert_raises(exceptions.ConnectionError):
            self.server.add(1, 2)

    def test_handle_response_none(self):
        with assert_raises(exceptions.ParseError):
            self.server.handle_response('{')
