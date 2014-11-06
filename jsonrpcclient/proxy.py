"""proxy.py"""

import os
import json
import logging
import pkgutil

import requests
import jsonschema

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
            logging.info('--> '+json.dumps(request_dict))

            try:
                # Send the message
                r = requests.post(
                    self.url,
                    headers={
                        'Content-Type': 'application/json; charset=utf-8'
                    },
                    json=request_dict
                )

                logging.info('<-- '+r.text.strip("\n"))

            except (requests.exceptions.InvalidSchema,
                    requests.exceptions.RequestException):
                raise exceptions.ConnectionError()

            # Raise exception if any HTTP response other than 200
#            if r.status_code != 200:
#                raise exceptions.StatusCodeError(r.status_code)

            # A response was expected, but none was given?
            if 'id' in request_dict and not len(r.text):
                raise exceptions.ReceivedNoResponse()

            # Was response given?
            if len(r.text):

                # Attempt to parse the response
                try:
                    response_dict = json.loads(r.text)

                except ValueError:
                    raise exceptions.ParseError()

                # A response was *not* expected, but one was given? It may not
                # be necessary to raise here. If we receive a response anyway,
                # can't we just ignore it?
                if 'id' not in request_dict and 'result' in response_dict:
                    raise exceptions.InvalidResponse()

                # Validate the response against the Response schema
                try:
                    jsonschema.validate(
                        response_dict,
                        json.loads(pkgutil.get_data(
                            __name__, 'response-schema.json').decode('utf-8')))

                except jsonschema.ValidationError:
                    raise exceptions.InvalidResponse()

                # If the response was "error", raise it, to ensure it's handled
                if 'error' in response_dict:
                    raise exceptions.ReceivedErrorResponse(
                        response_dict['error']['code'],
                        response_dict['error']['message'])

                # Otherwise, surely we have a result to return
                print(response_dict['result'])

            return None

        return handlerMethod
