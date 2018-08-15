"""
Exceptions.

These exceptions are raised when processing responses from the server. For
example, if the response was garbage and could not be parsed,
:class:`ParseResponseError <jsonrpcclient.exceptions.ParseResponseError>` is
raised.

To handle them, use a try-block when calling send/request/notify::

    try:
        client.notify('go')
    except JsonRpcClientError as e:
        ...
"""


class JsonRpcClientError(Exception):
    """Base class for the other exceptions."""

    pass


class ParseResponseError(JsonRpcClientError):
    """The response was not valid JSON."""

    def __init__(self) -> None:
        super().__init__("The response was not valid JSON")


class ReceivedNon2xxResponseError(JsonRpcClientError):
    """The response was not valid JSON."""

    def __init__(self, status_code: int) -> None:
        super().__init__("Received {} status code".format(status_code))
        self.code = status_code
