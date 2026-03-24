"""Tests for color resolution logic."""

import pytest

from tempeh.cli.state import ColorMode, resolve_color


@pytest.mark.parametrize(
    ("mode", "tty", "env", "expected"),
    [
        (ColorMode.always, False, {"NO_COLOR": "1"}, True),
        (ColorMode.never, True, {}, False),
        # auto: checks tty, NO_COLOR (https://no-color.org), TERM
        (ColorMode.auto, True, {}, True),
        (ColorMode.auto, False, {}, False),
        (ColorMode.auto, True, {"NO_COLOR": "1"}, False),
        (ColorMode.auto, True, {"NO_COLOR": ""}, True),
        (ColorMode.auto, True, {"TERM": "dumb"}, False),
        (ColorMode.auto, True, {"TERM": "DUMB"}, False),
    ],
)
def test_resolve_color(mode, tty, env, expected, monkeypatch):
    monkeypatch.setattr("sys.stdout", type("FakeStdout", (), {"isatty": lambda self: tty})())
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    assert resolve_color(mode) is expected
