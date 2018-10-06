# /usr/bin/env python
# pylint: disable=no-value-for-parameter
"""
This is an attempt at using this library to create a "jsonrpc" command-line utility.
Currently it's only useful for very basic requests.

$ pip install jsonrpcclient
$ jsonrpc ping
{"jsonrpc": "2.0", "method": "ping", "id": 1}
$ jsonrpc ping --send http://localhost:5000
{"jsonrpc": "2.0", "result": "pong", "id": 1}
"""
import sys
from typing import Any

import click
import pkg_resources

from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.exceptions import JsonRpcClientError
from jsonrpcclient.requests import Notification, Request

version = pkg_resources.require("jsonrpcclient")[0].version


@click.command(
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True}
)
@click.option("--id", default=1, help="Set the id for a request.")
@click.option(
    "--notify",
    "request_type",
    flag_value="notify",
    help="Indicates that no response is expected.",
)
@click.option("--send", help="URL to send request to. (requires the Requests library)")
@click.version_option(prog_name="jsonrpcclient", version=version)
@click.argument("method", required=True, metavar="METHOD [PARAMS]...")
@click.pass_context
def main(
    context: click.core.Context, method: str, request_type: str, id: Any, send: str
) -> None:
    """
    Create a JSON-RPC request.
    """
    exit_status = 0
    # Extract the jsonrpc arguments
    positional = [a for a in context.args if "=" not in a]
    named = {a.split("=")[0]: a.split("=")[1] for a in context.args if "=" in a}
    # Create the request
    if request_type == "notify":
        req = Notification(method, *positional, **named)
    else:
        req = Request(method, *positional, request_id=id, **named)  # type: ignore
    # Sending?
    if send:
        client = HTTPClient(send)
        try:
            response = client.send(req)
        except JsonRpcClientError as e:
            click.echo(str(e), err=True)
            exit_status = 1
        else:
            click.echo(response.text)
    # Otherwise, simply output the JSON-RPC request.
    else:
        click.echo(str(req))
    sys.exit(exit_status)


if __name__ == "__main__":
    main()
