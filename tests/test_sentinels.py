"""Test sentinels.py"""
# pylint: disable=missing-function-docstring
from jsonrpcclient.sentinels import Sentinel


def test_sentinel() -> None:
    assert repr(Sentinel("foo")) == "<foo>"
