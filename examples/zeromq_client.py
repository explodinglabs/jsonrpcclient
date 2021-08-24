from jsonrpcclient import request, parse, Ok
import json
import logging
import zmq

socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5000")
socket.send_string(request("ping"))

response = parse(json.loads(socket.recv().decode()))
if isinstance(response, Ok):
    print(response.result)
else:
    logging.error(response.message)
