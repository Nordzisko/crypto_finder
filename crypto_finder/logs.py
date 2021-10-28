"""
Configuration of structlog and code for ad-hoc processors.
"""
from time import time
from typing import Dict

import structlog
import structlog_pretty

from . import settings


def configure_structlog():
    """Set up structlog with one of two predefined config schemes.

    The config scheme is selected based on ``.settings.debug``.
    """
    processors = [
        drop_debug_logs,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        unix_timestamper,
        structlog_pretty.NumericRounder(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ]

    debug_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog_pretty.NumericRounder(),
        structlog.processors.TimeStamper("iso"),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.processors.UnicodeDecoder(),
        structlog.dev.ConsoleRenderer(pad_event=25),
    ]

    structlog.configure(
        processors=debug_processors if settings.DEBUG else processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )


def unix_timestamper(_, __, event_dict: Dict) -> Dict:
    """
    Add a ``timestamp`` key to the event dict with the current Unix time.
    """
    event_dict["timestamp"] = time() * 1000
    return event_dict


def drop_debug_logs(_, level: str, event_dict: Dict) -> Dict:
    """
    Drop the event if its level is ``debug``.
    """
    if level == "debug":
        raise structlog.DropEvent
    return event_dict
