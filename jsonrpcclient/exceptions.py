"""
Exceptions
**********

These exceptions are raised when processing responses from the server. For
example, if the response was garbage and could not be parsed,
:class:`ParseResponseError <jsonrpcclient.exceptions.ParseResponseError>` is
raised.

To handle them, use a try-block when calling ``notify`` or ``request``::

    try:
        server.notify('go')
    except JsonRpcClientError as e:
        print(str(e))
"""

class JsonRpcClientError(Exception):
    """Base class for the other exceptions."""

    pass


class ReceivedNoResponse(JsonRpcClientError):
    """A response message was expected, but none was given."""

    def __init__(self):
        super(ReceivedNoResponse, self).__init__(
            'No response was received')


class UnwantedResponse(JsonRpcClientError):
    """A response was not requested, but one was given anyway."""

    def __init__(self):
        super(UnwantedResponse, self).__init__(
            'An unwanted response was given')


class ParseResponseError(JsonRpcClientError):
    """The response was not valid JSON."""

    def __init__(self):
        super(ParseResponseError, self).__init__(
            'The response was not valid JSON')


class ReceivedErrorResponse(JsonRpcClientError):
    """Raised if a single JSON-RPC `error response object
    <http://www.jsonrpc.org/specification#error_object>`_ is received. *This is
    not raised for batch requests.*

    This error means one of two things:

    1. There was a problem with the request.
    2. There was a problem with the application at the receiving end.

    To see information about the error, catch the exception:

    .. code-block:: python
        :emphasize-lines: 5-6

        from jsonrpcclient.exceptions import JsonRpcClientError, \\
            ReceivedErrorResponse
        try:
            server.notify('go')
        except ReceivedErrorResponse as e:
            print(e.code, e.message, e.data)
        except JsonRpcClientError as e:
            print(str(e))
    """

    def __init__(self, code, message, data):
        """
        :param code: The JSON-RPC ``code`` value received.
        :param message: The JSON-RPC ``message`` value received.
        :param data: The JSON-RPC ``data`` value received.
        """
        super(ReceivedErrorResponse, self).__init__('; '.join(
            [item for item in [message, data] if item is not None]))
        #: The JSON-RPC status code. (See `status codes
        #: <http://www.jsonrpc.org/specification#error_object>`_.)
        self.code = code
        #: A one-line message explaining the error.
        self.message = message
        #: Extra information about the error, if given.
        self.data = data
