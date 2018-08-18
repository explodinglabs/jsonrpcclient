import logging
from jsonrpcclient.clients.http_client import HTTPClient

client = HTTPClient("http://localhost:5000")
response = client.request("ping")

if response.data.ok:
    print(response.data.result)
else:
    logging.error(response.data.message)
