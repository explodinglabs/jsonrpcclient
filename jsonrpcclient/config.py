import importlib
import os
from configparser import ConfigParser

from . import id_generators


def parse_callable(path: str):
    module = path[:path.rindex(".")]
    callable_name = path[path.rindex(".") + 1:]
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
