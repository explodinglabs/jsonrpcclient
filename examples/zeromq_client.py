from jsonrpcclient.zeromq_client import ZeroMQClient

response = ZeroMQClient('tcp://localhost:5000').request('ping')
print(type(response))
print(response)
