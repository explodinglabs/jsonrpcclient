"""Prepared request"""
import json
from past.builtins import basestring #pylint:disable=redefined-builtin

class PreparedRequest(str):
    """An object to validate and encapsulate a request before sending, which can
    be passed around subsequent methods. Subclasses of Client can add to it, or
    set the log format/extra info to include.

    Converts some non-string requests to string.
    """
    def __new__(cls, request):
        # Convert a list of strings, to one string
        if isinstance(request, list) and all(isinstance(i, basestring) for i in
                                             request):
            request = '[{}]'.format(', '.join(request))
        # Convert a json-serializable object (dict or list) to a string
        if not isinstance(request, basestring):
            request = json.dumps(request)
        # Should end up with a string
        assert isinstance(request, basestring)
        return str.__new__(cls, request)

    def __init__(self, request): #pylint:disable=unused-argument
        super(PreparedRequest, self).__init__()
        #: Extra details used in log entry, can be set by clients in
        #: _prepare_request
        self.log_extra = None
        self.log_format = None
