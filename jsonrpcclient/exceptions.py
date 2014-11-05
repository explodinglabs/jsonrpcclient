"""exceptions.py"""

class RPCClientException(Exception):
    """Base class for the other rpcclient exceptions"""
    pass

class ConnectionError(RPCClientException): # pylint: disable=redefined-builtin
    """The requests module raised an error, which could be a network issue,
    invalid HTTP response or timeout. See
    http://stackoverflow.com/questions/16511337/"""

    def __init__(self):
        super().__init__('Connection error')

class StatusCodeError(RPCClientException):
    """The server responded with status code != 200"""

    def __init__(self, status_code):
        super().__init__('Returned status code '+str(status_code))

class ParseError(RPCClientException):
    """Couldnt parse the json response (invalid json)"""

    def __init__(self):
        super().__init__('Parse error')

class InvalidResponse(RPCClientException):
    """The response didnt validate against the JSON-RPC response schema"""

    def __init__(self):
        super().__init__('Invalid response')

class ReceivedNoResponse(RPCClientException):
    """A response was expected, but no response was received"""

    def __init__(self):
        super().__init__('No response')

class ReceivedErrorResponse(RPCClientException):
    """The server responded with 'error'. Raise it so it must be handled"""

    def __init__(self, code, message): #pylint:disable=unused-argument
        super().__init__(message)
