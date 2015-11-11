"""__init__.py"""

import logging
logging.getLogger('jsonrpcclient').addHandler(logging.NullHandler())

from jsonrpcclient.request import Request
