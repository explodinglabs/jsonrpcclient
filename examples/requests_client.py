"""Requests client"""
import logging
import requests

from jsonrpcclient import request, parse, Ok, Error


response = requests.post("http://localhost:5000/", json=request("ping"), timeout=10)
parsed = parse(response.json())
if isinstance(parsed, Ok):
    print(parsed.result)
elif isinstance(parsed, Error):
    logging.error(parsed.message)
