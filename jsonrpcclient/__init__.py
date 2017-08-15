"""__init__.py"""
from .request import Request, Notification
from .http_client import HTTPClient


def request(endpoint, method, *args, **kwargs):
    """
    A convenience function. Instantiates and executes a HTTPClient request, then
    throws it away.
    """
    return HTTPClient(endpoint).request(method, *args, **kwargs)


def notify(endpoint, method, *args, **kwargs):
    """
    A convenience function. Instantiates and executes a HTTPClient request, then
    throws it away.
    """
    return HTTPClient(endpoint).notify(method, *args, **kwargs)
