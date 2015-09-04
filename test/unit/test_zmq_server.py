"""test_zmq_server.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

import json
from unittest import TestCase, main
import itertools

import zmq

from jsonrpcclient import rpc
from jsonrpcclient.rpc import rpc_request_str
from jsonrpcclient.zmq_server import ZMQServer


class TestZMQServer(TestCase):

    def setUp(self):
        rpc.id_generator = itertools.count(1) # Ensure the first generated is 1

    @staticmethod
    def test_instantiate():
        ZMQServer('tcp://localhost:5555')

    def test_send_message_with_connection_error(self):
        server = ZMQServer('tcp://localhost:5555')
        # Set timeouts
        server.socket.setsockopt(zmq.RCVTIMEO, 5)
        server.socket.setsockopt(zmq.SNDTIMEO, 5)
        server.socket.setsockopt(zmq.LINGER, 5)
        with self.assertRaises(zmq.error.ZMQError):
            server.send_message(json.dumps(rpc_request_str('go')))


if __name__ == '__main__':
    main()
