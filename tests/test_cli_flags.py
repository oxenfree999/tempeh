"""Tests for global CLI flags."""

from pathlib import Path

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
    result = runner.invoke(cli, ["doctor", "--json"])
    assert result.exit_code == 0


def test_config_error_missing_file() -> None:
    result = runner.invoke(cli, ["--config", "nonexistent.toml", "config"])
    assert result.exit_code == 1
    assert "Config error" in result.output


@pytest.mark.parametrize(
    ("toml_content", "match"),
    [
        ("invalid = = toml", "Config error"),
        ("[bogus]\nkey = 1", "unknown section"),
        ("[process]\nstop_timeout = 42", "expected str, got int"),
        ('[process]\nstop_timeout = "nope"', "invalid duration"),
    ],
)
def test_config_error_invalid_content(tmp_path: Path, toml_content: str, match: str) -> None:
    toml_file = tmp_path / "psoul.toml"
    toml_file.write_text(toml_content)
    result = runner.invoke(cli, ["--config", str(toml_file), "config"])
    assert result.exit_code == 1
    assert match in result.output


def test_help_shows_flags() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    output = typer.unstyle(result.output)
    for flag in ["--verbose", "--quiet", "--color", "--config", "--version"]:
        assert flag in output
