"""Global CLI state passed to all subcommands via ctx.obj."""

import os
import sys
from dataclasses import dataclass
from enum import Enum, IntEnum
from pathlib import Path


class ExitCode(IntEnum):
    SUCCESS = 0
    ERROR = 1
    USAGE = 2


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
    log_level: int
    config_path: Path | None
