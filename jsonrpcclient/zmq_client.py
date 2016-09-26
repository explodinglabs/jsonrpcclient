"""Deprecated module, remove in version 3"""
from warnings import warn

from .zeromq_client import ZeroMQClient


warn('ZMQClient is deprecated, use ZeroMQClient', DeprecationWarning)

class ZMQClient(ZeroMQClient):
    """Deprecate by subclassing"""
    pass
