import logging

from jsonrpcclient.clients.zeromq_client import ZeroMQClient
from jsonrpcclient.requests import Request, Notification


requests = [Request("ping"), Notification("ping"), Request("ping")]
response = ZeroMQClient("tcp://localhost:5000").send(requests)

for data in response.data:
    if data.ok:
        print("{}: {}".format(data.id, data.result))
    else:
        logging.error("%d: %s", data.id, data.message)
