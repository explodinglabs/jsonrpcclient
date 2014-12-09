# pylint: disable=missing-docstring,line-too-long,no-self-use
"""server_test.py"""

import unittest
import itertools

from jsonrpcclient.server import Server
from jsonrpcclient import rpc
from jsonrpcclient import exceptions


class TestServer(unittest.TestCase): # pylint: disable=too-many-public-methods

    def setUp(self):
        rpc.id_generator = itertools.count(1) # First generated is 1
        self.server = Server('http://non-existant/')

    def test_request(self):
        with self.assertRaises(exceptions.ConnectionError):
            self.server.request('add', 1, 2)

    def test_notify(self):
        with self.assertRaises(exceptions.ConnectionError):
            self.server.notify('add', 1, 2)

    def test_alternate_usage(self):
        with self.assertRaises(exceptions.ConnectionError):
            self.server.add(1, 2)

    def test_parse_error(self):
        with self.assertRaises(exceptions.ParseError):
            self.server.handle_response('{')
