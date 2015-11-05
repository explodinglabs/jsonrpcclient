from unittest import TestCase, main
import re
from uuid import UUID

from jsonrpcclient.id_iterators import hex_iterator, uuid_iterator, \
    random_iterator

class TestHexIterator(TestCase):

    def test(self):
        i = hex_iterator()
        self.assertEqual('1', next(i))
        i = hex_iterator(9)
        self.assertEqual('9', next(i))
        self.assertEqual('a', next(i))


class TestUUIDIterator(TestCase):

    def test(self):
        i = uuid_iterator()
        # Raise ValueError if badly formed hexadecimal UUID string
        UUID(next(i), version=4)


class TestRandomIterator(TestCase):

    def test(self):
        i = random_iterator()
        self.assertTrue(re.match('^[0-9,a-z]{8}$', next(i)))


if __name__ == '__main__':
    main()
