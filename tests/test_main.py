from json import JSONDecodeError
from unittest.mock import patch

from click.testing import CliRunner

from jsonrpcclient.__main__ import main


def test():
    result = CliRunner().invoke(main, "foo")
    assert result.exit_code == 0


def test_notify():
    result = CliRunner().invoke(main, ["foo", "--notify"])
    assert result.exit_code == 0


@patch("jsonrpcclient.__main__.HTTPClient.send")
def test_send(*_):
    result = CliRunner().invoke(main, ["foo", "--send=http://foo"])
    assert result.exit_code == 0


@patch("jsonrpcclient.__main__.HTTPClient.send", side_effect=JSONDecodeError)
def test_send_error(*_):
    result = CliRunner().invoke(main, ["foo", "--send=http://foo"])
    assert result.exit_code == -1
