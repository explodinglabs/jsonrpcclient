"""
ZMQServer
*********

Send JSON-RPC requests to a ZeroMQ server, for example::

    ZMQServer('tcp://hostname:5555').notify('go')
"""

import zmq

from jsonrpcclient.server import Server


class ZMQServer(Server):
    """
    :param endpoint: The server address.
    :param options: The socket type, which can be any of the zeromq socket
                    types. Default is *zmq.REQ*.
    """

    def __init__(self, endpoint, socket_type=zmq.REQ):
        super(ZMQServer, self).__init__(endpoint)
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    def send_message(self, request):
        """Send the request to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response (a string for requests, None for notifications).
        """
        self.log_request(request)
        self.socket.send_string(request)
        response = self.socket.recv().decode('UTF-8')
        self.log_response(response)
        return response
