import json
from past.builtins import basestring #pylint:disable=redefined-builtin

class PreparedRequest(str):
    """An object to validate and encapsulate a request before sending, which can
    be added to by subclasses of Client."""

    def __new__(cls, request):
        # Convert a json-serializable object to a string if it's not already
        if not isinstance(request, basestring):
            return str.__new__(cls, json.dumps(request))
        else:
            return str.__new__(cls, request)

    def __init__(self, request):
        #: Extra details used in log entry
        self.extras = None
