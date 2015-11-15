To see the JSON-RPC messages going back and forth, set the logging level to
``INFO``::

    import logging
    logging.getLogger('jsonrpcclient').setLevel(logging.INFO)

Then add a basic handler::

    logging.getLogger('jsonrpcclient').addHandler(logging.StreamHandler())

Or use custom handlers and formats::

    request_format = '%(endpoint)s --> %(message)s'
    response_format = '%(endpoint)s <-- %(message)s'

    # Request log
    request_handler = logging.StreamHandler()
    request_handler.setFormatter(logging.Formatter(fmt=request_format))
    logging.getLogger('jsonrpcclient.server.request').addHandler(
        request_handler)

    # Response log
    response_handler = logging.StreamHandler()
    response_handler.setFormatter(logging.Formatter(fmt=response_format))
    logging.getLogger('jsonrpcclient.server.response').addHandler(
        response_handler)
