"""test_zmq_server.py"""
#pylint:disable=missing-docstring,line-too-long,protected-access

from unittest import TestCase, main
import itertools

import zmq
from mock import patch, Mock

from jsonrpcclient import request
from jsonrpcclient.request import Request
from jsonrpcclient.zmq_server import ZMQServer


class TestZMQServer(TestCase):

    def setUp(self):
        # Monkey patch id_iterator to ensure the request id is always 1
        request.id_iterator = itertools.count(1)

    @staticmethod
    def test_instantiate():
        ZMQServer('tcp://localhost:5555')

    @patch('zmq.Socket.send_string', Mock())
    @patch('zmq.Socket.recv', Mock())
    def test_send_message(self): # pylint: disable=no-self-use
        server = ZMQServer('tcp://localhost:5555')
        server._send_message(str(Request('go')))

    def test_send_message_with_connection_error(self):
        server = ZMQServer('tcp://localhost:5555')
        # Set timeouts
        server.socket.setsockopt(zmq.RCVTIMEO, 5)
        server.socket.setsockopt(zmq.SNDTIMEO, 5)
        server.socket.setsockopt(zmq.LINGER, 5)
        with self.assertRaises(zmq.error.ZMQError):
            server._send_message(str(Request('go')))


if __name__ == '__main__':
    main()
