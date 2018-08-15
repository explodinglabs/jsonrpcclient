"""
An HTTP client.

For example::

    HTTPClient('http://example.com/api').request('go')

Uses the `Requests <http://docs.python-requests.org/en/master/>`_ library.
"""
from typing import Any, Iterable

from requests import Session

from ..client import Client
from ..exceptions import ReceivedNon2xxResponseError
from ..response import Response


class HTTPClient(Client):
    """Defines an HTTP client"""

    # The default HTTP header
    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        :param endpoint: The server address.
        :param **kwargs: Pased through to the Client class.
        """
        super().__init__(*args, **kwargs)
        # Make use of Requests' sessions feature
        self.session = Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def log_response(self, response: Response, fmt: str = None, **kwargs: Any) -> None:
        super().log_response(
            response,
            extra={
                "http_code": response.raw.status_code,  # type: ignore
                "http_reason": response.raw.reason,  # type: ignore
            },
            fmt="%(log_color)s\u27f5 %(message)s (%(http_code)s %(http_reason)s)",
            **kwargs
        )

    def validate_response(self, response: Response) -> None:
        if not 200 <= response.raw.status_code <= 299:  # type: ignore
            raise ReceivedNon2xxResponseError(response.raw.status_code)  # type: ignore

    def send_message(self, request: str, **kwargs: Any) -> Response:
        response = self.session.post(self.endpoint, data=request.encode(), **kwargs)
        return Response(response.text, raw=response)
