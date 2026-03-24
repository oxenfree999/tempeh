"""Tests for log-level resolution and structlog configuration."""

import logging

import pytest
import structlog

from tempeh.cli.logging import configure_logging, resolve_log_level
from tempeh.cli.state import OutputFormat


@pytest.mark.parametrize(
    ("verbose", "quiet", "env", "expected"),
    [
        (0, False, {}, logging.WARNING),
        (1, False, {}, logging.INFO),
        (2, False, {}, logging.DEBUG),
        (3, False, {}, logging.DEBUG),
        (0, True, {}, logging.ERROR),
        (0, False, {"TEMPEH_LOG": "debug"}, logging.DEBUG),
        (0, False, {"TEMPEH_LOG": "info"}, logging.INFO),
        (0, False, {"TEMPEH_LOG": "error"}, logging.ERROR),
        (0, False, {"TEMPEH_LOG": "DEBUG"}, logging.DEBUG),
        (1, False, {"TEMPEH_LOG": "error"}, logging.INFO),
        (0, True, {"TEMPEH_LOG": "debug"}, logging.ERROR),
        (0, False, {"TEMPEH_LOG": "bogus"}, logging.WARNING),
        (0, False, {"TEMPEH_LOG": ""}, logging.WARNING),
    ],
)
def test_resolve_log_level(verbose, quiet, env, expected, monkeypatch):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    assert resolve_log_level(verbose, quiet) == expected


@pytest.fixture(autouse=True)
def _reset_structlog():
    yield
    structlog.reset_defaults()


def test_output_to_stderr(capsys):
    configure_logging(logging.DEBUG, OutputFormat.text)
    structlog.get_logger().info("hello")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "hello" in captured.err


def test_json_output():
    configure_logging(logging.DEBUG, OutputFormat.json)
    with structlog.testing.capture_logs() as logs:
        structlog.get_logger().info("hello")
    assert logs == [{"event": "hello", "log_level": "info"}]


def test_level_filtering():
    configure_logging(logging.WARNING, OutputFormat.text)
    with structlog.testing.capture_logs() as logs:
        structlog.get_logger().info("should not appear")
        structlog.get_logger().warning("should appear")
    assert len(logs) == 1
    assert logs[0]["event"] == "should appear"
