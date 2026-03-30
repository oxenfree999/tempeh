"""Tests for psoul doctor command."""

import json
import shutil
import subprocess
import sys
from types import SimpleNamespace
from typing import Never

import pytest
from typer.testing import CliRunner

from psoul.cli.doctor import PREFERRED_TOOLS, _get_tool_info, _get_venv, format_text, get_system_info
from psoul.cli.main import cli

runner = CliRunner()


def test_get_tool_info_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/fake")
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout="fake 1.2.3\n"))
    assert _get_tool_info("fake") == {"available": True, "version": "1.2.3", "path": "/usr/bin/fake", "error": None}


def test_get_tool_info_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/fake")

    def run_timeout(*args: object, **kwargs: object) -> Never:
        raise subprocess.TimeoutExpired(cmd="fake", timeout=1)

    monkeypatch.setattr(subprocess, "run", run_timeout)
    assert _get_tool_info("fake") == {
        "available": True,
        "version": None,
        "path": "/usr/bin/fake",
        "error": "Command 'fake' timed out after 1 seconds",
    }


def test_get_tool_info_oserror(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/fake")

    def run_oserror(*args: object, **kwargs: object) -> Never:
        raise OSError("exec failed")

    monkeypatch.setattr(subprocess, "run", run_oserror)
    assert _get_tool_info("fake") == {
        "available": True,
        "version": None,
        "path": "/usr/bin/fake",
        "error": "exec failed",
    }


def test_get_tool_info_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda name: None)
    assert _get_tool_info("fake") == {"available": False, "version": None, "path": None, "error": None}


def test_get_venv_active(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "prefix", "/home/user/.venv")
    monkeypatch.setattr(sys, "base_prefix", "/usr/lib/python3")
    assert _get_venv() == "/home/user/.venv"


def test_get_venv_not_active(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "prefix", "/usr/lib/python3")
    monkeypatch.setattr(sys, "base_prefix", "/usr/lib/python3")
    assert _get_venv() is None


def test_get_system_info_keys() -> None:
    info = get_system_info()
    assert set(info.keys()) == {"platform", "directory", "venv", "interpreter", "python", "psoul", "tools"}


def test_format_text_shows_unavailable_tools() -> None:
    info = get_system_info()
    info["tools"]["ruff"] = {"available": False, "version": None, "path": None, "error": None}
    output = format_text(info)
    assert "ruff" in output
    assert "not found" in output


def test_doctor_text_contains_expected_labels() -> None:
    result = runner.invoke(cli, ["doctor"])
    assert result.exit_code == 0
    for label in ("Platform", "Directory", "Venv", "Interpreter", "psoul", "Python", *PREFERRED_TOOLS):
        assert label in result.output


def test_doctor_json_is_valid() -> None:
    result = runner.invoke(cli, ["doctor", "--json"])
    assert result.exit_code == 0
    assert isinstance(json.loads(result.output), dict)
