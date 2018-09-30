from jsonrpcclient.clients.http_client import HTTPClient

client = HTTPClient("http://localhost:5000")
response = client.request("ping")
print(response.data.result)
