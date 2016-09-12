"""test_zmq_client.py"""
#pylint:disable=missing-docstring,line-too-long,protected-access

from unittest import TestCase, main
import itertools

import zmq
from mock import patch, Mock

from jsonrpcclient import Request
from jsonrpcclient.zmq_client import ZMQClient


class TestZMQClient(TestCase):

    def setUp(self):
        # Patch Request.id_iterator to ensure the request id is always 1
        Request.id_iterator = itertools.count(1)

    @staticmethod
    def test_instantiate():
        ZMQClient('tcp://localhost:5555')

    @patch('zmq.Socket.send_string', Mock())
    @patch('zmq.Socket.recv', Mock())
    def test_send_message(self): # pylint: disable=no-self-use
        client = ZMQClient('tcp://localhost:5555')
        client._send_message(str(Request('go')))

    def test_send_message_with_connection_error(self):
        client = ZMQClient('tcp://localhost:5555')
        # Set timeouts
        client.socket.setsockopt(zmq.RCVTIMEO, 5)
        client.socket.setsockopt(zmq.SNDTIMEO, 5)
        client.socket.setsockopt(zmq.LINGER, 5)
        with self.assertRaises(zmq.error.ZMQError):
            client._send_message(str(Request('go')))


if __name__ == '__main__':
    main()
