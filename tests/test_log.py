import json
from unittest import TestCase
from jsonrpcclient.log import trim_message


class TestTrim(TestCase):
    def test_string_abbreviation(self):
        message = trim_message("blah" * 100)
        self.assertIn("...", message)

    def test_list_abbreviation(self):
        message = trim_message(json.dumps({"list": [0] * 100}))
        self.assertIn("...", message)

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
        self.assertIn("...", json.loads(message)["obj"]["obj2"]["string2"])
