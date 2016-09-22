from jsonrpcclient.http_client import HTTPClient

response = HTTPClient('http://localhost:5000/').request('ping')
print(response)
