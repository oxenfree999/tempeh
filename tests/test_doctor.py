"""Tests for tempeh doctor command."""

import json
import shutil
import subprocess
import sys
from types import SimpleNamespace

from typer.testing import CliRunner

from tempeh.cli.doctor import _get_tool_info, _get_venv, get_system_info
from tempeh.cli.main import cli

runner = CliRunner()


def test_get_tool_info_found(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/fake")
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout="fake 1.2.3\n"))
    assert _get_tool_info("fake") == {"available": True, "version": "1.2.3", "path": "/usr/bin/fake"}


def test_get_tool_info_not_found(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    assert _get_tool_info("fake") == {"available": False, "version": None, "path": None}


def test_get_venv_active(monkeypatch):
    monkeypatch.setattr(sys, "prefix", "/home/user/.venv")
    monkeypatch.setattr(sys, "base_prefix", "/usr/lib/python3")
    assert _get_venv() == "/home/user/.venv"


def test_get_venv_not_active(monkeypatch):
    monkeypatch.setattr(sys, "prefix", "/usr/lib/python3")
    monkeypatch.setattr(sys, "base_prefix", "/usr/lib/python3")
    assert _get_venv() is None


def test_get_system_info_keys():
    info = get_system_info()
    assert set(info.keys()) == {"platform", "directory", "venv", "interpreter", "python", "tempeh", "uv", "ruff", "ty"}


def test_doctor_exits_zero():
    result = runner.invoke(cli, ["doctor"])
    assert result.exit_code == 0


def test_doctor_json_is_valid():
    result = runner.invoke(cli, ["--json", "doctor"])
    assert result.exit_code == 0
    assert isinstance(json.loads(result.output), dict)
