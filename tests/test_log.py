import json
import logging
from unittest.mock import patch, Mock
from jsonrpcclient.log import configure_logger, _trim_string, _trim_values


class TestConfigureLogger:
    def test(self):
        configure_logger(Mock(level=logging.NOTSET), "%s")

    @patch("jsonrpcclient.log.logging.root.handlers", None)
    def test_no_handlers(self, *_):
        configure_logger(Mock(level=logging.NOTSET, handlers=None), "%s")


def test_trim_string():
    message = _trim_string("foo" * 100)
    assert "..." in message


def test_trim_values():
    message = _trim_values({"list": [0] * 100})
    assert "..." in message["list"]


def test_trim_values_nested():
    message = _trim_values({"obj": {"obj2": {"string2": "foo" * 100}}})
    assert "..." in message["obj"]["obj2"]["string2"]
