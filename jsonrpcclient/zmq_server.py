"""Deprecated module, remove in version 3"""
from warnings import warn

from .zeromq_client import ZeroMQClient


warn('ZMQServer is deprecated, use ZeroMQClient', DeprecationWarning)

class ZMQServer(ZeroMQClient):
    """Deprecate by subclassing"""
    pass
