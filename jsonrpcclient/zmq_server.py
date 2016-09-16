"""Deprecated module, remove in version 3"""
from warnings import warn

from jsonrpcclient.zmq_client import ZMQClient


warn('ZMQServer is deprecated, use ZMQClient', DeprecationWarning)

class ZMQServer(ZMQClient):
    """Deprecate by subclassing"""
    pass
