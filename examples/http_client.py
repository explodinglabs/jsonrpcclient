from jsonrpcclient.clients.http_client import HTTPClient

response = HTTPClient("http://localhost:5000/").request("ping")

if response.result.ok:
    print(response.data.result)
else:
    print("Error: {}".format(response.data.message))
