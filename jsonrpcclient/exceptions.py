"""exceptions.py

The string passed to the Exception class can be accessed like ``str(e)``::

    >>> try:
    ...     s.request('add', 1)
    ... except JsonRpcClientError as e:
    ...     print(str(e))
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


class InvalidResponse(JsonRpcClientError):
    """The response was not a valid JSON-RPC response."""
    def __init__(self):
        super(InvalidResponse, self).__init__(
            'The response was not a valid JSON-RPC 2.0 response')


class ReceivedErrorResponse(JsonRpcClientError):
    """The server gave a valid JSON-RPC error response."""
    def __init__(self, code, message, data): #pylint:disable=unused-argument
        super(ReceivedErrorResponse, self).__init__(
            'The server gave a valid JSON-RPC error response: '+message)
        self.code = code
        self.message = message
        self.data = data
