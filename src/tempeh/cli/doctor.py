"""Environment health checks for tempeh doctor."""

import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from tempeh.version import VERSION

LABEL_WIDTH = 14


def _shorten_path(path: str) -> str:
    """Replace home directory with ~ for shorter display."""
    home = str(Path.home())
    return path.replace(home, "~", 1) if path.startswith(home) else path


def _get_tool_info(name: str) -> dict[str, Any]:
    """Detect a CLI tool's availability and version."""
    path = shutil.which(name)
    if path is None:
        return {"available": False, "version": None, "path": None}
    proc = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
    version = proc.stdout.strip().removeprefix(f"{name} ").split()[0] if proc.returncode == 0 else None
    return {"available": True, "version": version, "path": path}


def _get_venv() -> str | None:
    """Return the venv path if running inside a virtual environment."""
    return sys.prefix if sys.prefix != sys.base_prefix else None


def get_system_info() -> dict[str, Any]:
    """Collect environment information."""
    return {
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "directory": str(Path.cwd()),
        "venv": _get_venv(),
        "interpreter": sys.executable,
        "python": {"version": platform.python_version()},
        "tempeh": {"version": VERSION},
        "uv": _get_tool_info("uv"),
        "ruff": _get_tool_info("ruff"),
        "ty": _get_tool_info("ty"),
    }


def format_text(info: dict[str, Any]) -> str:
    """Format system info as aligned text."""
    lines = []

    p = info["platform"]
    lines.append(f"{'Platform':<{LABEL_WIDTH}} {p['system']} {p['release']} ({p['machine']})")
    lines.append(f"{'Directory':<{LABEL_WIDTH}} {_shorten_path(info['directory'])}")

    venv = info["venv"]
    lines.append(f"{'Venv':<{LABEL_WIDTH}} {_shorten_path(venv) if venv else 'not active'}")
    lines.append(f"{'Interpreter':<{LABEL_WIDTH}} {_shorten_path(info['interpreter'])}")

    lines.append(f"{'Tempeh':<{LABEL_WIDTH}} {info['tempeh']['version']}")
    lines.append(f"{'Python':<{LABEL_WIDTH}} {info['python']['version']}")

    for name in ("uv", "ruff", "ty"):
        tool = info[name]
        if tool["available"]:
            lines.append(f"{name:<{LABEL_WIDTH}} {tool['version']}")

    return "\n".join(lines)
