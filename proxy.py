"""proxy.py"""

import os
import json
import logging
import requests

from standard.dictfuncs import validate_dict_against_schema_file
from standard.dictfuncs import ValidationErrors
from . import rpc
from . import exceptions

class Proxy:
    """This class acts as the remote server"""

    def __init__(self, url):
        self.url = url

    def __getattr__(self, name):
        """Catch undefined methods and handle them as RPC requests.

        The technique is here:
        http://code.activestate.com/recipes/307618/
        """

        def handlerMethod(*args, **kwargs):
            """Send the RPC request to the proxy server.

            Calls a procedure on another server.
            Raises RPCClientException: On any error caught.
            """

            # Construct an rpc request from the method name and other arguments
            # passed
            request_dict = rpc.request(name, *args, **kwargs)

            # Log the request
            logging.getLogger('main').info('--> '+json.dumps(request_dict))

            try:
                # Send the message
                r = requests.post(
                    self.url,
                    headers={
                        'Content-Type': 'application/json; charset=utf-8'
#                        'Signature': 'Amtek Web Service',
#                        'Identity': 'ED5A8F2E-4D9F-4589-B842-3C8AB2EC3F04'
                    },
                    json=request_dict
                )

                logging.getLogger('main').info('<-- '+r.text.strip("\n"))

            except (requests.exceptions.InvalidSchema,
                    requests.exceptions.RequestException):
                raise exceptions.ConnectionError()

            # Raise exception if any HTTP response other than 200
            if r.status_code != 200:
                raise exceptions.StatusCodeError(r.status_code)

            # A response was expected, but none was given?
            if 'id' in request_dict and not len(r.text):
                raise exceptions.ReceivedNoResponse()

            # A response was *not* expected, but one was given?
            if 'id' not in request_dict and len(r.text):
                raise exceptions.InvalidResponse()

            # Was response given?
            if len(r.text):

                # Attempt to parse the response
                try:
                    response_dict = json.loads(r.text)

                except ValueError:
                    raise exceptions.ParseError()

                # Validate the response against the Response schema
                try:
                    validate_dict_against_schema_file(
                        response_dict,
                        os.path.dirname(__file__)+'/schemas/Response.json')

                except ValidationErrors:
                    raise exceptions.InvalidResponse()

                # Ensure the "id" in the response matches the request id
                # Can't - the id might be null for some errors
                #if not response_dict['id'] == request_dict['id']:
                #    raise exceptions.InvalidResponse()

                # If the response was "error", raise it, to ensure it's handled
                if 'error' in response_dict:
                    raise exceptions.ReceivedErrorResponse(
                        response_dict['error']['code'],
                        response_dict['error']['message'])

                # Otherwise, surely we have a result to return
                return response_dict['result']

            return None

        return handlerMethod
