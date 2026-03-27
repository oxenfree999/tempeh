"""Tests for global CLI flags."""

import pytest
import typer
from typer.testing import CliRunner

from psoul.cli.main import cli
from psoul.version import VERSION

runner = CliRunner()


@pytest.mark.parametrize("args", [["--version"], ["-V"], ["version"]])
def test_version_output(args: list[str]) -> None:
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert f"psoul {VERSION}" in result.output


def test_verbose_quiet_conflict() -> None:
    result = runner.invoke(cli, ["-v", "-q", "version"])
    assert result.exit_code != 0
    assert "cannot be used together" in result.output


def test_color_invalid() -> None:
    result = runner.invoke(cli, ["--color", "bogus", "version"])
    assert result.exit_code != 0


def test_json_shorthand() -> None:
    result = runner.invoke(cli, ["--json", "version"])
    assert result.exit_code == 0


def test_help_shows_flags() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    output = typer.unstyle(result.output)
    for flag in ["--verbose", "--quiet", "--color", "--format", "--config", "--version"]:
        assert flag in output
