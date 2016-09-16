"""Deprecated module, remove in version 3"""
from abc import abstractmethod

from jsonrpcclient.client import Client


class Server(Client):
    """Deprecate by subclassing"""

    @abstractmethod
    def _send_message(self, request, **kwargs):
        """Must be overridden"""
