from jsonrpcclient import request_json, parse_json, Ok
import logging
import zmq

socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5000")
socket.send_string(request_json("ping"))

response = parse_json(socket.recv().decode())
if isinstance(response, Ok):
    print(response.result)
else:
    logging.error(response.message)
