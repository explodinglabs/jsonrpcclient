from .request import Request, Notification
from .clients.http_client import HTTPClient


def notify(
    endpoint,
    method,
    *args,
    trim_log_values=False,
    validate_against_schema=True,
    **kwargs
):
    """
    A convenience function. Instantiates and executes a HTTPClient request, then
    throws it away.
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
    A convenience function. Instantiates and executes a HTTPClient request, then
    throws it away.
    """
    return HTTPClient(
        endpoint,
        id_generator=id_generator,
        trim_log_values=trim_log_values,
        validate_against_schema=validate_against_schema,
    ).request(method, *args, **kwargs)
