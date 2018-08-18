import logging
import sys

from jsonrpcclient.clients.zeromq_client import ZeroMQClient

response = ZeroMQClient("tcp://localhost:5000").request("ping")

if response.data.ok:
    print(response.data.result)
else:
    logging.error(response.data.message)
