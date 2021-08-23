from jsonrpcclient import request_dict, parse, Ok, Error
import logging
import requests

response = requests.post("http://localhost:5000/", json=request_dict("ping"))

# Python 3.10 syntax
match parse(response.json()):
    case Ok(result, id):
        print(result)
    case Error(code, message, data, id):
        logging.error(message)
