# Convenience functions
from jsonrpcclient.response import Response


def request(endpoint: str, *args: list, **kwargs: dict) -> Response:
    from .clients.http_client import HTTPClient

    return HTTPClient(endpoint).request(*args, **kwargs)


def notify(endpoint: str, *args: list, **kwargs: dict) -> Response:
    from .clients.http_client import HTTPClient

    return HTTPClient(endpoint).request(*args, **kwargs)


def send(endpoint: str, *args: list, **kwargs: dict) -> Response:
    from .clients.http_client import HTTPClient

    return HTTPClient(endpoint).send(*args, **kwargs)
