"""
ZeroMQClient
*********

A ZeroMQ client to send requests::

    ZMQClient('tcp://hostname:5555').request('go')
"""

import zmq

from jsonrpcclient.client import Client


class ZeroMQClient(Client):
    """
    :param endpoint: The server address.
    :param socket_type: The zeromq `socket type`_. Default is *zmq.REQ*.
    """

    def __init__(self, endpoint, socket_type=zmq.REQ): # pylint: disable=no-member
        super(ZeroMQClient, self).__init__(endpoint)
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    def _send_message(self, request):
        """Transport the message to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response (a string for requests, None for notifications).
        """
        self.socket.send_string(request)
        response = self.socket.recv().decode()
        return self._process_response(response)
