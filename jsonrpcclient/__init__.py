"""__init__.py"""

import logging

logger = logging.getLogger('jsonrpcclient')
logger.addHandler(logging.StreamHandler())

from jsonrpcclient.server import Server
