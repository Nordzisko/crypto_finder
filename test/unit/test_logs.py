import pytest
import structlog

from crypto_finder import logs


def test_unix_timestamper(mocker):
    mocker.patch("crypto_finder.logs.time", return_value=1234567890.0)
    result = logs.unix_timestamper(None, None, {})
    assert result == {"timestamp": 1234567890000.0}


def test_drop_debug_logs_on_info():
    param = {"level": "info"}
    result = logs.drop_debug_logs(None, "info", param)
    assert result == param


def test_drop_debug_logs_on_debug():
    param = {"level": "debug"}
    with pytest.raises(structlog.DropEvent):
        logs.drop_debug_logs(None, "debug", param)
