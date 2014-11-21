"""__init__.py"""

import logging

logger = logging.getLogger('jsonrpcclient')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

from jsonrpcclient.server import Server
