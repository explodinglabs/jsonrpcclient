# Convenience functions

def request(endpoint, *args, **kwargs):
    from .clients.http_client import HTTPClient
    return HTTPClient(endpoint).request(*args, **kwargs)


def notify(endpoint, *args, **kwargs):
    from .clients.http_client import HTTPClient
    return HTTPClient(endpoint).request(*args, **kwargs)


def send(endpoint, *args, **kwargs):
    from .clients.http_client import HTTPClient
    return HTTPClient(endpoint).send(*args, **kwargs)
