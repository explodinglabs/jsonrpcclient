"""exceptions.py"""


class JsonRpcClientError(Exception):
    """Base class for the other exceptions"""
    pass


class InvalidRequest(JsonRpcClientError):
    """The request being sent is not valid json."""

    def __init__(self):
        super().__init__('The request you\'re sending is not valid json')


class ConnectionError(JsonRpcClientError): # pylint: disable=redefined-builtin
    """There was a network issue, invalid HTTP response or timeout."""

    def __init__(self):
        super().__init__('Connection error')


class Non200Response(JsonRpcClientError):
    """The server responded with a HTTP status code other than 200."""

    def __init__(self, status_code):
        super().__init__('Returned status code '+str(status_code))


class ReceivedNoResponse(JsonRpcClientError):
    """A response message was expected, but none was given."""

    def __init__(self):
        super().__init__('No response was received')


class UnwantedResponse(JsonRpcClientError):
    """A response was not requested, but one was given anyway."""

    def __init__(self):
        super().__init__('An unwanted response was given')


class ParseResponseError(JsonRpcClientError):
    """The response was not valid json."""

    def __init__(self):
        super().__init__('The response was not valid json')


class InvalidResponse(JsonRpcClientError):
    """The response was not a valid JSON-RPC response."""

    def __init__(self):
        super().__init__('The response was not a valid json-rpc 2.0 response')


class ReceivedErrorResponse(JsonRpcClientError):
    """The server gave a valid JSON-RPC *error* response."""

    def __init__(self, code, message): #pylint:disable=unused-argument
        super().__init__(message)
