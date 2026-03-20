"""Global CLI state passed to all subcommands via ctx.obj."""

import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ColorMode(str, Enum):
    auto = "auto"
    always = "always"
    never = "never"


class OutputFormat(str, Enum):
    text = "text"
    json = "json"


def resolve_color(mode: ColorMode) -> bool:
    """Decide whether to emit color based on --color choice and environment."""
    if mode is ColorMode.always:
        return True
    if mode is ColorMode.never:
        return False
    return sys.stdout.isatty() and os.environ.get("NO_COLOR", "") == "" and os.environ.get("TERM", "").lower() != "dumb"


@dataclass(frozen=True, slots=True)
class GlobalState:
    verbose: int
    quiet: bool
    color: ColorMode
    color_enabled: bool
    output_format: OutputFormat
    config_path: Path | None
