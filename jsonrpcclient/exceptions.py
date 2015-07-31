"""exceptions.py"""


class JsonRpcClientError(Exception):
    """Base class for the other exceptions"""
    pass


class InvalidRequest(JsonRpcClientError):
    """The request being sent is not valid JSON."""
    pass


class ConnectionError(JsonRpcClientError): # pylint: disable=redefined-builtin
    """There was a network issue, invalid HTTP response or timeout."""
    pass


class ReceivedNoResponse(JsonRpcClientError):
    """A response message was expected, but none was given."""
    pass


class UnwantedResponse(JsonRpcClientError):
    """A response was not requested, but one was given anyway."""
    pass


class ParseResponseError(JsonRpcClientError):
    """The response was not valid json."""
    pass


class InvalidResponse(JsonRpcClientError):
    """The response was not a valid JSON-RPC response."""
    pass


class ReceivedErrorResponse(JsonRpcClientError):
    """The server gave a valid JSON-RPC *error* response."""
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data
