"""Tempeh CLI entry point."""

import json
from pathlib import Path
from typing import Annotated

import typer

from tempeh.cli.doctor import format_text, get_system_info
from tempeh.cli.logging import configure_logging, resolve_log_level
from tempeh.cli.state import ColorMode, GlobalState, OutputFormat, resolve_color
from tempeh.version import VERSION

cli = typer.Typer(
    name="tempeh",
    help="A CLI and TUI Python session supervisor with batteries included.",
    invoke_without_command=True,
    context_settings={"help_option_names": ["--help", "-h"]},
)


def _version_callback(value: bool) -> None:
    if value:
        print(f"tempeh {VERSION}")
        raise typer.Exit()


@cli.callback()
def _main(
    ctx: typer.Context,
    verbose: Annotated[int, typer.Option("--verbose", "-v", count=True, help="Increase output detail (-v, -vv).")] = 0,
    quiet: Annotated[bool, typer.Option("--quiet", "-q", help="Suppress non-essential output.")] = False,
    color: Annotated[ColorMode, typer.Option("--color", help="Color mode.", case_sensitive=False)] = ColorMode.auto,
    output_format: Annotated[
        OutputFormat, typer.Option("--format", help="Output format.", case_sensitive=False)
    ] = OutputFormat.text,
    json_flag: Annotated[bool, typer.Option("--json", help="Shorthand for --format json.")] = False,
    config: Annotated[Path | None, typer.Option("--config", help="Override config file location.")] = None,
    version: Annotated[
        bool | None, typer.Option("--version", "-V", callback=_version_callback, is_eager=True, help="Show version.")
    ] = None,
) -> None:
    if verbose and quiet:
        raise typer.BadParameter("--verbose and --quiet cannot be used together.")

    if json_flag:
        output_format = OutputFormat.json

    log_level = resolve_log_level(verbose, quiet)

    ctx.obj = GlobalState(
        verbose=verbose,
        quiet=quiet,
        color=color,
        color_enabled=resolve_color(color),
        output_format=output_format,
        log_level=log_level,
        config_path=config,
    )

    configure_logging(log_level, output_format)

    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
        raise typer.Exit()


@cli.command()
def doctor(ctx: typer.Context) -> None:
    """Check Tempeh environment and report status."""
    info = get_system_info()
    state: GlobalState = ctx.obj
    if state.output_format == OutputFormat.json:
        print(json.dumps(info, indent=2))
    else:
        print(format_text(info))


@cli.command()
def version() -> None:
    """Show Tempeh version."""
    print(f"tempeh {VERSION}")
