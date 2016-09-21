from jsonrpcclient.http_client import HTTPClient

HTTPClient('http://localhost:5000/').request('ping')
