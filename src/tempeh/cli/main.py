"""Tempeh CLI entry point."""

import typer

from tempeh.version import VERSION

cli = typer.Typer(
    name="tempeh",
    help="A CLI and TUI Python session supervisor with batteries included.",
    invoke_without_command=True,
)


@cli.callback()
def _main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
        raise typer.Exit()


@cli.command()
def version() -> None:
    """Show Tempeh version."""
    print(f"tempeh {VERSION}")
