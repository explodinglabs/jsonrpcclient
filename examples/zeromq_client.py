from jsonrpcclient.zeromq_client import ZeroMQClient

response = ZeroMQClient('tcp://localhost:5000').ping()
print(response)
