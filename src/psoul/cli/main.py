"""psoul CLI entry point."""

import dataclasses
import json
import sys
import tomllib
from pathlib import Path
from typing import Annotated

import typer

from psoul.cli.doctor import format_text, get_system_info
from psoul.cli.logging import configure_logging, resolve_log_level
from psoul.cli.state import ColorMode, ExitCode, GlobalState, OutputFormat, resolve_color
from psoul.config import PsoulConfig, find_config_file, generate_config, load_config
from psoul.version import VERSION

cli = typer.Typer(
    name="psoul",
    help="A CLI and TUI Python session supervisor with batteries included.",
    invoke_without_command=True,
    context_settings={"help_option_names": ["--help", "-h"]},
)


def _load_resolved_config(config_override: Path | None) -> PsoulConfig:
    try:
        config_file = find_config_file(config_override)
        return load_config(config_file)
    except (FileNotFoundError, tomllib.TOMLDecodeError, TypeError, ValueError) as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        raise typer.Exit(ExitCode.ERROR) from exc


def _version_callback(value: bool) -> None:
    if value:
        print(f"psoul {VERSION}")
        raise typer.Exit(ExitCode.SUCCESS)


@cli.callback()
def _main(
    ctx: typer.Context,
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True, help="Increase output detail (-v, -vv).")] = 0,
    quiet: Annotated[bool, typer.Option("--quiet", "-q", help="Suppress non-essential output.")] = False,
    color: Annotated[ColorMode, typer.Option("--color", help="Color mode.", case_sensitive=False)] = ColorMode.auto,
    config: Annotated[Path | None, typer.Option("--config", help="Override config file location.")] = None,
    version: Annotated[  # noqa: ARG001 — Typer requires the param; work happens in callback
        bool | None, typer.Option("--version", "-V", callback=_version_callback, is_eager=True, help="Show version.")
    ] = None,
) -> None:
    if verbose and quiet:
        raise typer.BadParameter("--verbose and --quiet cannot be used together.")

    log_level = resolve_log_level(verbose, quiet)

    ctx.obj = GlobalState(
        verbose=verbose,
        quiet=quiet,
        color=color,
        color_enabled=resolve_color(color),
        log_level=log_level,
        config_override=config,
    )

    configure_logging(log_level, OutputFormat.text)

    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
        raise typer.Exit(ExitCode.SUCCESS)


@cli.command()
def doctor(
    json_flag: Annotated[bool, typer.Option("--json", help="Output JSON instead of text.")] = False,
) -> None:
    """Check psoul environment and report status."""
    info = get_system_info()
    if json_flag:
        print(json.dumps(info, indent=2))
    else:
        print(format_text(info))


config_app = typer.Typer(name="config", help="Show and manage configuration.")
cli.add_typer(config_app, name="config")


@config_app.callback(invoke_without_command=True)
def config_cmd(
    ctx: typer.Context,
    default: Annotated[bool, typer.Option("--default", help="Show default configuration.")] = False,
    json_flag: Annotated[bool, typer.Option("--json", help="Output JSON instead of text.")] = False,
) -> None:
    """Show and manage configuration."""
    if ctx.invoked_subcommand is not None:
        return
    state: GlobalState = ctx.obj
    cfg = PsoulConfig() if default else _load_resolved_config(state.config_override)
    data = dataclasses.asdict(cfg)
    if json_flag:
        print(json.dumps(data, indent=2, default=str))
    else:
        for section, values in data.items():
            for key, value in values.items():
                print(f"{section}.{key} = {value!r}")


@config_app.command()
def init(ctx: typer.Context) -> None:
    """Write a default psoul.toml to the current directory."""
    dest = Path("psoul.toml")
    if dest.exists():
        print(f"Error: {dest} already exists.", file=sys.stderr)
        raise typer.Exit(ExitCode.ERROR)
    dest.write_text(generate_config())
    state: GlobalState = ctx.obj
    if not state.quiet:
        print(f"Wrote {dest}")


@cli.command()
def version() -> None:
    """Show psoul version."""
    print(f"psoul {VERSION}")
