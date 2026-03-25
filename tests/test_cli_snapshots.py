"""Snapshot tests for CLI help and version output.

These tests lock the exact text of every help screen and the version
string.  When the CLI surface changes intentionally, run:

    uv run pytest tests/test_cli_snapshots.py --inline-snapshot=update

to accept the new output.
"""

import typer
from inline_snapshot import snapshot
from typer.testing import CliRunner

from tempeh.cli.main import cli

runner = CliRunner()

# Rich uses rounded corners on Unix/macOS but square corners on legacy
# Windows.  Normalize to square so snapshots are platform-agnostic.
_BOX_NORMALIZE = str.maketrans("╭╮╰╯", "┌┐└┘")


def normalize_box(text: str) -> str:
    return text.translate(_BOX_NORMALIZE)


def test_main_help(monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert normalize_box(typer.unstyle(result.output)) == snapshot("""\
                                                                                \n\
 Usage: tempeh [OPTIONS] COMMAND [ARGS]...                                      \n\
                                                                                \n\
 A CLI and TUI Python session supervisor with batteries included.               \n\
                                                                                \n\
┌─ Options ────────────────────────────────────────────────────────────────────┐
│ --verbose             -v      INTEGER              Increase output detail    │
│                                                    (-v, -vv).                │
│                                                    [default: 0]              │
│ --quiet               -q                           Suppress non-essential    │
│                                                    output.                   │
│ --color                       [auto|always|never]  Color mode.               │
│                                                    [default: auto]           │
│ --format                      [text|json]          Output format.            │
│                                                    [default: text]           │
│ --json                                             Shorthand for --format    │
│                                                    json.                     │
│ --config                      PATH                 Override config file      │
│                                                    location.                 │
│ --version             -V                           Show version.             │
│ --install-completion                               Install completion for    │
│                                                    the current shell.        │
│ --show-completion                                  Show completion for the   │
│                                                    current shell, to copy it │
│                                                    or customize the          │
│                                                    installation.             │
│ --help                -h                           Show this message and     │
│                                                    exit.                     │
└──────────────────────────────────────────────────────────────────────────────┘
┌─ Commands ───────────────────────────────────────────────────────────────────┐
│ doctor   Check Tempeh environment and report status.                         │
│ version  Show Tempeh version.                                                │
└──────────────────────────────────────────────────────────────────────────────┘

""")


def test_version_help(monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")
    result = runner.invoke(cli, ["version", "--help"])
    assert result.exit_code == 0
    assert normalize_box(typer.unstyle(result.output)) == snapshot("""\
                                                                                \n\
 Usage: tempeh version [OPTIONS]                                                \n\
                                                                                \n\
 Show Tempeh version.                                                           \n\
                                                                                \n\
┌─ Options ────────────────────────────────────────────────────────────────────┐
│ --help  -h        Show this message and exit.                                │
└──────────────────────────────────────────────────────────────────────────────┘

""")


def test_doctor_help(monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")
    result = runner.invoke(cli, ["doctor", "--help"])
    assert result.exit_code == 0
    assert normalize_box(typer.unstyle(result.output)) == snapshot("""\
                                                                                \n\
 Usage: tempeh doctor [OPTIONS]                                                 \n\
                                                                                \n\
 Check Tempeh environment and report status.                                    \n\
                                                                                \n\
┌─ Options ────────────────────────────────────────────────────────────────────┐
│ --help  -h        Show this message and exit.                                │
└──────────────────────────────────────────────────────────────────────────────┘

""")


def test_version_output():
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert result.output == snapshot("tempeh 0.0.1\n")
