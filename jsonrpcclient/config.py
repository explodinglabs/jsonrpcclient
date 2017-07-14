"""
Configure the jsonrpcclient package.

Import this module to to configure, for example::

    from jsonrpcclient import config
    config.validate = False
"""
#: Configure the ``id`` part of requests. Can be "decimal", "hex", "random" or
#: "uuid".
ids = 'decimal'

#: Validate responses against the JSON-RPC schema. Disable to speed up
#: processing.
validate = True
