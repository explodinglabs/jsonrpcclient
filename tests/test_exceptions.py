import pytest

from jsonrpcclient import exceptions


def test_parse_response_error():
    with pytest.raises(exceptions.ParseResponseError):
        raise exceptions.ParseResponseError


def test_non_2xx_status_code_error():
    with pytest.raises(exceptions.ReceivedNon2xxResponseError):
        raise exceptions.ReceivedNon2xxResponseError(404)
