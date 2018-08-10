"""
An HTTP client.

For example::

    HTTPClient('http://example.com/api').request('go')

Uses the `Requests <http://docs.python-requests.org/en/master/>`_ library.
"""
from requests import Request, Session

from ..client import Client
from ..exceptions import ReceivedNon2xxResponseError
from ..response import Response


class HTTPClient(Client):
    """Defines an HTTP client"""

    # The default HTTP header
    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, *args, **kwargs):
        """
        :param endpoint: The server address.
        :param **kwargs: Pased through to the Client class.
        """
        super().__init__(*args, **kwargs)
        # Make use of Requests' sessions feature
        self.session = Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def log_response(self, response):
        super().log_response(
            response,
            fmt="<-- %(message)s (%(http_code)s %(http_reason)s)",
            extra={
                "http_code": response.raw.status_code,
                "http_reason": response.raw.reason,
            },
        )

    def validate_response(self, response):
        if not 200 <= response.raw.status_code <= 299:
            raise ReceivedNon2xxResponseError(response.raw.status_code)

    def send_message(self, request, **kwargs):
        response = self.session.post(self.endpoint, data=request, **kwargs)
        return Response(response.text, raw=response)


def notify(
    endpoint,
    method,
    *args,
    trim_log_values=False,
    validate_against_schema=True,
    **kwargs
):
    """
    Convenience function - instantiates and executes a HTTPClient to perform a request,
    then throws it away.
    """
    return HTTPClient(
        endpoint,
        trim_log_values=trim_log_values,
        validate_against_schema=validate_against_schema,
    ).notify(method, *args, **kwargs)


def request(
    endpoint,
    method,
    *args,
    id_generator=None,
    trim_log_values=False,
    validate_against_schema=True,
    **kwargs
):
    """
    Convenience function - instantiates and executes a HTTPClient to perform a request,
    then throws it away.
    """
    return HTTPClient(
        endpoint,
        id_generator=id_generator,
        trim_log_values=trim_log_values,
        validate_against_schema=validate_against_schema,
    ).request(method, *args, **kwargs)
