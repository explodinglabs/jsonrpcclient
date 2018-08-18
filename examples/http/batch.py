import logging

from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.request import Request

client = HTTPClient("http://localhost:5000")
response = client.send([Request("ping"), Request("ping"), Request("ping")])

for data in response.data:
    if data.ok:
        print("{}: {}".format(data.id, data.result))
    else:
        logging.error("%d: %s", data.id, data.message)
