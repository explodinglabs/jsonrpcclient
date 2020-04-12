from json import JSONDecodeError
from unittest.mock import patch

import click
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


def get_click_exception_return_code():
    # The reason for this is that in click 7.0 the return code for an Exception changed
    # from -1 to 1
    click_version_major = int(click.__version__.split(sep='.')[0])
    if click_version_major < 7:
        return -1
    return 1


@patch("jsonrpcclient.__main__.HTTPClient.send", side_effect=JSONDecodeError)
def test_send_error(*_):
    result = CliRunner().invoke(main, ["foo", "--send=http://foo"])
    assert result.exit_code == get_click_exception_return_code()
