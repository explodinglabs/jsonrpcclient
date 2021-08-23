from jsonrpcclient import request_dict, parse, Ok
import logging
import requests

response = requests.post("http://localhost:5000/", json=request_dict("ping"))

parsed = parse(response.json())
if isinstance(parsed, Ok):
    print(parsed.result)
else:
    logging.error(parsed.message)
