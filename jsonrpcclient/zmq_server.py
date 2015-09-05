"""zmq_server.py"""

import zmq

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
        """Send the request to the server and return the response.

        :param request: The JSON-RPC request string.
        :return: The response (a string for requests, None for notifications).
        """
        self.log_request(request)
        self.socket.send_string(request)
        response = self.socket.recv().decode('UTF-8')
        self.log_response(response)
        return response
