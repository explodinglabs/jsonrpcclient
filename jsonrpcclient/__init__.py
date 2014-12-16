"""__init__.py"""

from logging import getLogger, StreamHandler

request_log = getLogger('jsonrpcclient.request')
response_log = getLogger('jsonrpcclient.response')

from jsonrpcclient.server import Server
