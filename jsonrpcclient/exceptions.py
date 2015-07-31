"""exceptions.py

The string passed to the Exception class can be accessed like ``str(e)``::

    >>> try:
    ...     s.request('add', 1)
    ... except JsonRpcClientError as e:
    ...     print(str(e))
    ...
    The server gave a valid JSON-RPC error response
    >>>

"""


class JsonRpcClientError(Exception):
    """Base class for the other exceptions."""
    pass


class InvalidRequest(JsonRpcClientError):
    """The request being sent is not valid JSON."""
    def __init__(self):
        super(InvalidRequest, self).__init__(
            'The request being sent is not valid json')


class ConnectionError(JsonRpcClientError): # pylint: disable=redefined-builtin
    """There was a network issue, invalid HTTP response or timeout."""
    def __init__(self):
        super(ConnectionError, self).__init__(
            'Connection error')


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
    """The response was not valid json."""
    def __init__(self):
        super(ParseResponseError, self).__init__(
            'The response was not valid json')


class InvalidResponse(JsonRpcClientError):
    """The response was not a valid JSON-RPC response."""
    def __init__(self):
        super(InvalidResponse, self).__init__(
            'The response was not a valid json-rpc 2.0 response')


class ReceivedErrorResponse(JsonRpcClientError):
    """The server gave a valid JSON-RPC error response."""
    def __init__(self, code, message, data): #pylint:disable=unused-argument
        super(ReceivedErrorResponse, self).__init__(
            'The server gave a valid JSON-RPC error response')
        self.code = code
        self.message = message
        self.data = data
