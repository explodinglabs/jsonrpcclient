"""By default the request ``id`` is a decimal number which increments with each
request. See the :mod:`config` module.
"""
import itertools
from string import digits, ascii_lowercase
from random import choice
from uuid import uuid4


def decimal(start=1):
    """Increments from ``start``, e.g. 1, 2, 3, .. 9, 10, 11, etc.

    :param start: The first value to start with.
    """
    return itertools.count(start)

def hexadecimal(start=1):
    """Incremental hexadecimal numbers. e.g. 1, 2, 3, .. 9, a, b, etc.

    :param start: The first value to start with.
    """
    while True:
        yield '%x' % start
        start += 1


def random(length=8, chars=digits+ascii_lowercase):
    """A random string - not unique, but has around 1 in a million chance of
    collision (with the default 8 character length). e.g. 'fubui5e6'

    :param length: Length of the random string.
    :param chars: The characters to randomly choose from.
    """
    while True:
        yield ''.join([choice(chars) for _ in range(length)])


def uuid():
    """Unique uuid ids. e.g. '9bfe2c93-717e-4a45-b91b-55422c5af4ff'"""
    while True:
        yield str(uuid4())


def from_config(setting):
    """Returns an iterator, based on a configuration setting, such as
    'decimal'
    """
    # Create iterator based on config setting
    if setting == 'decimal':
        return decimal()
    elif setting == 'hex':
        return hexadecimal()
    elif setting == 'random':
        return random()
    elif setting == 'uuid':
        return uuid()
    else:
        raise ValueError('Unknown ids config setting')
