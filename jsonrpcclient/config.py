"""Some options are configured in the ``config`` module. Import it and modify
the attributes. For example::

    from jsonrpcclient import config
    config.validate = False
"""
#: Validate responses against the JSON-RPC schema. Disable to speed up
#: processing.
validate = True
