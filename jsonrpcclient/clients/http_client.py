"""
An HTTP client.

For example:

    HTTPClient('http://example.com/api').request('go')

Uses the Requests library.
http://docs.python-requests.org/en/master/
"""
from typing import Any

from requests import Session

from ..client import Client
from ..exceptions import ReceivedNon2xxResponseError
from ..response import Response


class HTTPClient(Client):
    """Defines an HTTP client"""

    # The default HTTP header
    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
    DEFAULT_RESPONSE_LOG_FORMAT = "<-- %(message)s (%(http_code)s %(http_reason)s)"

    def __init__(self, endpoint: str, *args: Any, **kwargs: Any) -> None:
        """
        Args:
            endpoint: The server address.
        """
        super().__init__(*args, **kwargs)
        self.endpoint = endpoint
        # Make use of Requests' sessions feature
        self.session = Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def log_response(self, response: Response, **kwargs: Any) -> None:
        extra = (
            {"http_code": response.raw.status_code, "http_reason": response.raw.reason}
            if response.raw is not None
            else {}
        )
        super().log_response(response, extra=extra, **kwargs)

    def validate_response(self, response: Response) -> None:
        if response.raw is not None and not 200 <= response.raw.status_code <= 299:
            raise ReceivedNon2xxResponseError(response.raw.status_code)

    def send_message(
        self, request: str, response_expected: bool, **kwargs: Any
    ) -> Response:
        """
        Transport the message to the server and return the response.

        Args:
            request: The JSON-RPC request string.
            response_expected: Whether the request expects a response.

        Returns:
            A Response object.
        """
        response = self.session.post(self.endpoint, data=request.encode(), **kwargs)
        return Response(response.text, raw=response)
