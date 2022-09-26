from jsonrpcclient import request, parse, Ok, Error
import logging
import requests

response = requests.post("http://localhost:5000/", json=request("ping"))

parsed = parse(response.json())
if isinstance(parsed, Ok):
    print(parsed.result)
elif isinstance(parsed, Error):
    logging.error(parsed.message)
