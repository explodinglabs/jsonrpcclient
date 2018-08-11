"""Logging"""
import json
import logging
from typing import List, Dict, Optional, Union, Any, cast
import colorlog  # type: ignore


def configure_logger(logger: logging.Logger, fmt: str) -> None:
    """
    Set up a logger, if no handler has been configured for it.

    Used by the log function below.
    """
    if not logging.root.handlers and not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(fmt=fmt))
        logger.addHandler(handler)


def _trim_string(message: str) -> str:
    longest_string = 30

    if len(message) > longest_string:
        prefix_len = int(longest_string / 3)
        suffix_len = prefix_len
        return message[:prefix_len] + "..." + message[-suffix_len:]

    return message


def _trim_dict(message_obj: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    longest_list = 30
    for k, val in message_obj.items():
        if isinstance(val, str):
            result[k] = _trim_string(val)
        elif isinstance(val, list) and len(val) > longest_list:
            prefix_len = int(longest_list / 3)
            suffix_len = prefix_len
            result[k] = cast(str, val[:prefix_len] + ["..."] + val[-suffix_len:])
        elif isinstance(val, dict):
            result[k] = cast(str, _trim_values(val))
        else:
            result[k] = val
    return result


def _trim_values(message_obj: Union[Dict, List]) -> Union[Dict, List]:
    # Batch?
    if isinstance(message_obj, list):
        return [_trim_dict(i) for i in message_obj]
    else:
        return _trim_dict(message_obj)


def trim_message(message: str) -> str:
    try:
        message_obj = json.loads(message)
        return json.dumps(_trim_values(message_obj))
    except ValueError:
        return _trim_string(str(message))


def log_(
    message: str,
    logger: logging.Logger,
    level: str = "info",
    extra: Optional[Dict] = None,
    fmt: str = "%(message)s",
    trim: bool = False,
) -> None:
    """
    Log a request or response

    :param message: JSON-RPC request or response string.
    """
    if extra is None:
        extra = {}
    # Clean up the message for logging
    if message:
        message = message.replace("\n", "").replace("  ", " ").replace("{ ", "{")
    if trim:
        message = trim_message(message)
    configure_logger(logger, fmt)
    getattr(logger, level)(message, extra=extra)
