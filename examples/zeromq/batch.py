import logging
import sys

from jsonrpcclient.clients.zeromq_client import ZeroMQClient
from jsonrpcclient.request import Request

requests = [Request("ping"), Request("ping"), Request("ping")]
response = ZeroMQClient("tcp://localhost:5000").send(requests)

for data in response.data:
    if data.ok:
        print("{}: {}".format(data.id, data.result))
    else:
        logging.error("%d: %s", data.id, data.message)
