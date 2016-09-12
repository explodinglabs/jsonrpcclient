"""Deprecated module, remove in version 3"""
from warnings import warn

from jsonrpcclient.client import Client


class Server(Client):
    pass
