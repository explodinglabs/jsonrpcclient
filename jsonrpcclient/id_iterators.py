"""
ID Iterators
************

The default "id" part of a request is a decimal number which increments starting
from 1::

    >>> Request('go', response=True)
    {'jsonrpc': '2.0', 'method': 'get', 'id': 1}
    >>> Request('go', response=True)
    {'jsonrpc': '2.0', 'method': 'get', 'id': 2}

The ids can be changed to different formats if you prefer::

    >>> from jsonrpcclient.request import Request
    >>> from jsonrpcclient.id_iterators import random_iterator
    >>> Request.id_iterator = random_iterator()
    >>> Request('go', response=True)
    {'jsonrpc': '2.0', 'method': 'get', 'id': 'fubui5e6'}
"""

from uuid import uuid4
from string import digits, ascii_lowercase
from random import choice


def hex_iterator(start=1):
    """Incremental hexadecimal numbers.

    e.g. '1', '2'..'8a2f', etc.

    ::

        Request.id_iterator = hex_iterator()
    """
    while True:
        yield '%x' % start
        start += 1


def uuid_iterator():
    """Unique uuid ids.

    e.g. '9bfe2c93-717e-4a45-b91b-55422c5af4ff'

    ::

        Request.id_iterator = uuid_iterator()
    """
    while True:
        yield str(uuid4())


def random_iterator(length=8, chars=digits+ascii_lowercase):
    """A random string. Not unique, but has around 1 in a million chance of
    collision (with default values).

    e.g. 'fubui5e6'

    ::

        Request.id_iterator = random_iterator(16, 'abc123')

    :param length: Length of the random string.
    :param chars: The characters to randomly choose from.
    """
    while True:
        yield ''.join([choice(chars) for i in range(length)])
