#/usr/bin/env python
import pkg_resources

import click

from jsonrpcclient import request, notify
from jsonrpcclient.request import Request, Notification
from jsonrpcclient.http_client import HTTPClient


logo = """   ""
   88 ,adPPYba,  ,adPPYba,  8b,dPPYba,  8b,dPPYba, 8b,dPPYba,   ,adPPYba,
   88 I8[    "" a8"     "8a 88P'   `"8a 88P'   "Y8 88P'    "8a a8"     ""
   88  `"Y8ba,  8b       d8 88       88 88         88       d8 8b
   88 aa    ]8I "8a,   ,a8" 88       88 88         88b,   ,a8" "8a,   ,aa
   88 `"YbbdP"'  `"YbbdP"'  88       88 88         88`YbbdP"'   `"Ybbd8"'
  ,88                                              88
888P"        %(prog)s, version %(version)s          88"""
version = pkg_resources.require('jsonrpcclient')[0].version


@click.command(context_settings={'ignore_unknown_options': True, 'allow_extra_args': True})
@click.option('--id', default=1, help='Set the id for a request.')
@click.option('--notify', 'request_type', flag_value='notify', help='Indicates that no response is expected.')
@click.option('--send', help='URL to send request to. (requires the Requests library)')
@click.version_option(prog_name='jsonrpcclient', version=version, message=logo)
@click.argument('method', required=True, metavar='METHOD [PARAMS]...')
@click.pass_context
def main(context, method, request_type, id, send):
    """
    Create a JSON-RPC request.
    """
    # Extract the jsonrpc arguments
    positional = [a for a in context.args if '=' not in a]
    named = {a.split('=')[0]: a.split('=')[1] for a in context.args if '=' in a}
    # Create the request
    if request_type == 'notify':
        req = Notification(method, *positional, **named)
    else:
        req = Request(method, request_id=id, *positional, **named)
    # Sending?
    if send:
        response = HTTPClient(send).send(req)
        click.echo(response)
    # Otherwise, simply output the JSON-RPC request.
    else:
        click.echo(str(req))


if __name__ == '__main__':
    main()
