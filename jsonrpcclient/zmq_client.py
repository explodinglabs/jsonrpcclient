"""
ZMQClient
*********

A ZeroMQ client to communicate with, for example::

    ZMQClient('tcp://hostname:5555').request('go')

.. _socket type:
    https://zeromq.github.io/pyzmq/api/zmq.html#zmq.Context.socket
"""

import zmq

from jsonrpcclient.client import Client


class ZMQClient(Client):
    """
    :param endpoint: The server address.
    :param socket_type: The zeromq `socket type`_. Default is *zmq.REQ*.
    """

    def __init__(self, endpoint, socket_type=zmq.REQ): # pylint: disable=no-member
        super(ZMQClient, self).__init__(endpoint)
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    def _send_message(self, request):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response (a string for requests, None for notifications).
        """
        self.socket.send_string(request)
        response = self.socket.recv()
        return self._process_response(response.decode())
