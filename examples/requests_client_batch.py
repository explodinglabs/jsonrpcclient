"""Requests client - batching"""
import logging

import requests
from jsonrpcclient import request, parse, Ok, Error


response = requests.post(
    "http://localhost:5000/", json=[request("ping") for _ in range(5)], timeout=10
)

parsed = parse(response.json())
for p in parsed:
    if isinstance(p, Ok):
        print(p.result)
    elif isinstance(p, Error):
        logging.error(p.message)
