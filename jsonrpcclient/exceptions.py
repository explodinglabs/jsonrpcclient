"""exceptions.py"""


class JsonRpcClientError(Exception):
    """Base class for the other exceptions"""
    pass


class ConnectionError(JsonRpcClientError): # pylint: disable=redefined-builtin
    """The requests module raised an error, which could be a network issue,
    invalid HTTP response or timeout. See
    http://stackoverflow.com/questions/16511337/"""

    def __init__(self):
        super().__init__('Connection error')


class InvalidRequest(JsonRpcClientError):
    """The request you've sent is not valid json"""

    def __init__(self):
        super().__init__('The request you\'re sending is not valid json')


class Non200Response(JsonRpcClientError):
    """The server responded with status code != 200"""

    def __init__(self, status_code):
        super().__init__('Returned status code '+str(status_code))


class ParseResponseError(JsonRpcClientError):
    """Couldnt parse the json response (invalid json)"""

    def __init__(self):
        super().__init__('The response was not valid json')


class InvalidResponse(JsonRpcClientError):
    """The response didnt validate against the json-rpc response schema"""

    def __init__(self):
        super().__init__('The response was not a valid json-rpc 2.0 response')


class UnwantedResponse(JsonRpcClientError):
    """The response didnt validate against the json-rpc response schema"""

    def __init__(self):
        super().__init__('The response was not asked for')


class ReceivedNoResponse(JsonRpcClientError):
    """A response was expected, but no response was received"""

    def __init__(self):
        super().__init__('No response was received')


class ReceivedErrorResponse(JsonRpcClientError):
    """The server responded with 'error'. Raise it so it must be handled"""

    def __init__(self, code, message): #pylint:disable=unused-argument
        super().__init__(message)
