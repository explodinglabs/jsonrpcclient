"""Prepared request"""
import json
from past.builtins import basestring #pylint:disable=redefined-builtin

class PreparedRequest(str):
    """An object to validate and encapsulate a request before sending, which can
    be passed around subsequent methods. Subclasses of Client can add to it, or
    set the log format/extra info to include.
    """
    def __new__(cls, request):
        # Convert a json-serializable object to a string if it's not already
        if not isinstance(request, basestring):
            return str.__new__(cls, json.dumps(request))
        else:
            return str.__new__(cls, request)

    def __init__(self, request):
        super(PreparedRequest, self).__init__()
        #: Extra details used in log entry, can be set by clients in
        #: _prepare_request
        self.log_extra = None
        self.log_format = None
