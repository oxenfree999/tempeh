"""Tests for log-level resolution and structlog configuration."""

import json
import logging

import pytest
import structlog

from psoul.cli.logging import configure_logging, resolve_log_level
from psoul.cli.state import OutputFormat


@pytest.mark.parametrize(
    ("verbose", "quiet", "env", "expected"),
    [
        (0, False, {}, logging.WARNING),
        (1, False, {}, logging.INFO),
        (2, False, {}, logging.DEBUG),
        (3, False, {}, logging.DEBUG),
        (0, True, {}, logging.ERROR),
        (0, False, {"PSOUL_LOG": "debug"}, logging.DEBUG),
        (0, False, {"PSOUL_LOG": "info"}, logging.INFO),
        (0, False, {"PSOUL_LOG": "error"}, logging.ERROR),
        (0, False, {"PSOUL_LOG": "DEBUG"}, logging.DEBUG),
        (1, False, {"PSOUL_LOG": "error"}, logging.INFO),
        (0, True, {"PSOUL_LOG": "debug"}, logging.ERROR),
        (0, False, {"PSOUL_LOG": "bogus"}, logging.WARNING),
        (0, False, {"PSOUL_LOG": ""}, logging.WARNING),
    ],
)
def test_resolve_log_level(
    verbose: int, quiet: bool, env: dict[str, str], expected: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    assert resolve_log_level(verbose, quiet) == expected


def test_output_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(logging.DEBUG, OutputFormat.text)
    structlog.get_logger().info("hello")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "hello" in captured.err


def test_json_output() -> None:
    configure_logging(logging.DEBUG, OutputFormat.json)
    with structlog.testing.capture_logs() as logs:
        structlog.get_logger().info("hello")
    assert logs == [{"event": "hello", "log_level": "info"}]


def test_level_filtering() -> None:
    configure_logging(logging.WARNING, OutputFormat.text)
    with structlog.testing.capture_logs() as logs:
        structlog.get_logger().info("should not appear")
        structlog.get_logger().warning("should appear")
    assert len(logs) == 1
    assert logs[0]["event"] == "should appear"


def test_json_output_end_to_end(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(logging.DEBUG, OutputFormat.json)
    structlog.get_logger().info("hello")
    captured = capsys.readouterr()
    assert captured.out == ""
    parsed = json.loads(captured.err)
    assert parsed["event"] == "hello"
    assert parsed["level"] == "info"
