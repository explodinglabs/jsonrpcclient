from jsonrpcclient.zmq_client import ZMQClient

response = ZMQClient('tcp://localhost:5000').ping()
print(response)
