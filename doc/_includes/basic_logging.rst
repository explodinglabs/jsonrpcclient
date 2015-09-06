The JSON-RPC messages are logged on the ``INFO`` log level. To see them::

    import logging
    logging.getLogger('jsonrpcclient').setLevel(logging.INFO)

    logging.basicConfig() # Creates a basic StreamHandler with a default format
