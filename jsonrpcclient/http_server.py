"""Deprecated module, remove in version 3"""
from warnings import warn

from .http_client import HTTPClient


warn('HTTPServer is deprecated, use HTTPClient', DeprecationWarning)

class HTTPServer(HTTPClient):
    """Deprecate by subclassing"""
    pass
