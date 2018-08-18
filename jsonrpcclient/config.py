"""
Config object.

Allows modules to import a pre-loaded configuration object.
"""
import importlib
import os
from configparser import ConfigParser
from typing import Iterator


def parse_callable(path: str) -> Iterator:
    """
    ConfigParser converter.

    Calls the specified object, e.g. Option "id_generators.decimal" returns
    `id_generators.decimal()`.
    """
    module = path[: path.rindex(".")]
    callable_name = path[path.rindex(".") + 1 :]
    callable_ = getattr(importlib.import_module(module), callable_name)
    return callable_()


defaults = {
    "trim_log_values": "False",
    "validate_against_schema": "True",
    "id_generator": "jsonrpcclient.id_generators.decimal",
}
config = ConfigParser(
    defaults=defaults,
    default_section="general",
    converters={"callable": parse_callable},
)
config.read([".jsonrpcclientrc", os.path.expanduser("~/.jsonrpcclientrc")])
