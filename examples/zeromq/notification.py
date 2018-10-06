from jsonrpcclient.clients.zeromq_client import ZeroMQClient

response = ZeroMQClient("tcp://localhost:5000").notify("ping")
print(response.data.result)
