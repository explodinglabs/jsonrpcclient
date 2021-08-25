from jsonrpcclient import request, parse, Ok
import logging
import requests

response = requests.post(
    "http://localhost:5000/", json=[request("ping") for _ in range(5)]
)

parsed = parse(response.json())
for p in parsed:
    if isinstance(p, Ok):
        print(p.result)
    else:
        logging.error(p.message)
