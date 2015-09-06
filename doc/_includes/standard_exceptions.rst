jsonrpcclient.exceptions.ReceivedNoResponse
    A response message was expected, but none was given.

jsonrpcclient.exceptions.UnwantedResponse
    A response was not requested, but one was given.

jsonrpcclient.exceptions.ParseResponseError
    The response was not valid JSON.

jsonschema.ValidationError
    The response was not a valid JSON-RPC response object.

jsonrpcclient.exceptions.ReceivedErrorResponse
    The server gave a valid `JSON-RPC error response <http://www.jsonrpc.org/specification#error_object>`_.

The ``ReceivedErrorResponse`` exception has extra details, if you need them::

    from jsonrpcclient.exceptions import ReceivedErrorResponse
    try:
        server.request('go')
    except ReceivedErrorResponse as e:
        print(e.code, e.message, e.data)
