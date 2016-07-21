"""__init__.py"""

import logging

from jsonrpcclient.request import Request

logging.getLogger('jsonrpcclient').addHandler(logging.NullHandler())
