"""Requests client - Python 3.10 usage"""
import logging

import requests

from jsonrpcclient import Error, Ok, parse, request

response = requests.post("http://localhost:5000/", json=request("ping"), timeout=10)

# Python 3.10 syntax
match parse(response.json()):
    case Ok(result, id_):
        print(result)
    case Error(code, message, data, id_):
        logging.error(message)
