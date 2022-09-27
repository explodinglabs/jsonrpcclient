"""Websockets client"""
import logging

import requests
from jsonrpcclient import request, parse, Ok, Error

response = requests.post("http://localhost:5000/", json=request("ping"), timeout=10)

# Python 3.10 syntax
match parse(response.json()):
    case Ok(result, id_):
        print(result)
    case Error(code, message, data, id_):
        logging.error(message)
