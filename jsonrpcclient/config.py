"""Some options can be configured in the ``config`` module. Import it and modify
the attributes, for example::

    from jsonrpcclient import config
    config.validate = False
"""
#: Validate responses against the JSON-RPC schema. Disable to speed up
#: processing.
validate = True

#: Configure the ``id`` part of requests. Can be "decimal", "hex", "random" or
#: "uuid".
ids = 'decimal'
