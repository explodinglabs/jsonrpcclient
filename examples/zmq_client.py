from jsonrpcclient.zmq_client import ZMQClient

ZMQClient('tcp://localhost:5000').ping()
