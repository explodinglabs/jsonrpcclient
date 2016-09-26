"""Deprecated module, remove in version 3"""
from warnings import warn

from .tornado_client import TornadoClient


warn('TornadoServer is deprecated, use TornadoClient', DeprecationWarning)

class TornadoServer(TornadoClient):
    """Deprecate by subclassing"""
    pass
