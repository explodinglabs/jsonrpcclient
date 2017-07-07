"""test_ids.py"""
from unittest import TestCase, main
import re
from uuid import UUID

from jsonrpcclient import ids


class TestHexIterator(TestCase):
    def test(self):
        i = ids.hexadecimal()
        self.assertEqual('1', next(i))
        i = ids.hexadecimal(9)
        self.assertEqual('9', next(i))
        self.assertEqual('a', next(i))


class TestRandomIterator(TestCase):
    def test(self):
        i = ids.random()
        self.assertTrue(re.match('^[0-9,a-z]{8}$', next(i)))


class TestUUIDIterator(TestCase):
    def test(self):
        i = ids.uuid()
        # Raise ValueError if badly formed hexadecimal UUID string
        UUID(next(i), version=4)


if __name__ == '__main__':
    main()
