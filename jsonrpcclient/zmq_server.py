"""zmq_server.py"""

import zmq
import json

from .server import Server


class ZMQServer(Server):
    """Encapsulates a ZMQ server"""

    def __init__(self, endpoint, socket_type=zmq.REQ):
        """Connect to the ZMQ socket.

        Example usage::

            >>> server = ZMQServer('tcp://hostname:5555', zmq.REQ)

        :param endpoint: The remote server address.
        :param options: Socket options, see
            http://api.zeromq.org/2-1:zmq-setsockopt
        """
        super(ZMQServer, self).__init__(endpoint)
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.socket.connect(endpoint)

    def send_message(self, request):
        """Transport the request to the server and return the response.

        :param request: The JSON-RPC request, in dict format.
        :return: The response (a string for requests, None for notifications).
        """
        self.log_request(json.dumps(request))
        self.socket.send_string(json.dumps(request))
        response = self.socket.recv().decode('UTF-8')
        self.log_response(response)
        return response
