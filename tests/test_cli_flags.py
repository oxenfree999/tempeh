"""Tests for global CLI flags."""

import pytest
from typer.testing import CliRunner

from tempeh.cli.main import cli
from tempeh.version import VERSION

runner = CliRunner()


@pytest.mark.parametrize("args", [["--version"], ["-V"], ["version"]])
def test_version_output(args):
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert f"tempeh {VERSION}" in result.output


def test_verbose_quiet_conflict():
    result = runner.invoke(cli, ["-v", "-q", "version"])
    assert result.exit_code != 0
    assert "cannot be used together" in result.output


def test_color_invalid():
    result = runner.invoke(cli, ["--color", "bogus", "version"])
    assert result.exit_code != 0


def test_json_shorthand():
    result = runner.invoke(cli, ["--json", "version"])
    assert result.exit_code == 0


def test_help_shows_flags():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for flag in ["--verbose", "--quiet", "--color", "--format", "--config", "--version"]:
        assert flag in result.output
