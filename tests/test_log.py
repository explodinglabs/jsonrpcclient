import json
import logging
from unittest.mock import patch, Mock
from jsonrpcclient.log import configure_logger, trim_message


class TestConfigureLogger():
    def test(self):
        configure_logger(Mock(level=logging.NOTSET), "%s")

    @patch("jsonrpcclient.log.logging.root.handlers", None)
    def test_no_handlers(self, *_):
        configure_logger(Mock(level=logging.NOTSET, handlers=None), "%s")


class TestTrimMessage():
    def test_string_abbreviation(self):
        message = trim_message("blah" * 100)
        assert "..." in message

    def test_list_abbreviation(self):
        message = trim_message(json.dumps({"list": [0] * 100}))
        assert "..." in message

    def test_nested_abbreviation(self):
        message = trim_message(
            json.dumps(
                {
                    "obj": {
                        "list": [0] * 100,
                        "string": "blah" * 100,
                        "obj2": {"string2": "blah" * 100},
                    }
                }
            )
        )
        assert "..." in json.loads(message)["obj"]["obj2"]["string2"]
