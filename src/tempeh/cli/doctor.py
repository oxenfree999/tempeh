"""Environment health checks for tempeh doctor."""

import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from tempeh.version import VERSION

LABEL_WIDTH = 14

KNOWN_TOOLS = (
    "uv", "pip", "poetry", "pdm",               # packaging
    "ruff", "flake8", "pylint",                 # linting
    "black", "isort",                           # formatting
    "ty", "mypy", "pyright",                    # type checking
    "debugpy",                                  # debugging
    "austin", "py-spy", "memray", "scalene",    # profiling
)

PREFERRED_TOOLS = ("uv", "ruff", "ty", "debugpy")


def _get_tool_info(name: str) -> dict[str, Any]:
    """Detect a CLI tool's availability and version."""
    path = shutil.which(name)
    if path is None:
        return {"available": False, "version": None, "path": None}
    try:
        proc = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=3)
    except (subprocess.TimeoutExpired, OSError):
        return {"available": True, "version": None, "path": path}
    version = proc.stdout.strip().removeprefix(f"{name} ").split()[0] if proc.returncode == 0 else None
    return {"available": True, "version": version, "path": path}


def _get_venv() -> str | None:
    """Return the venv path if running inside a virtual environment."""
    return sys.prefix if sys.prefix != sys.base_prefix else None


def get_system_info() -> dict[str, Any]:
    """Collect environment information."""
    tools = {name: _get_tool_info(name) for name in KNOWN_TOOLS}
    return {
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "directory": str(Path.cwd()),
        "venv": _get_venv(),
        "interpreter": sys.executable,
        "python": {"version": platform.python_version()},
        "tempeh": {"version": VERSION},
        "tools": tools,
    }


def format_text(info: dict[str, Any]) -> str:
    """Format system info as aligned text."""
    lines = []

    p = info["platform"]
    lines.append(f"{'Platform':<{LABEL_WIDTH}} {p['system']} {p['release']} ({p['machine']})")
    lines.append(f"{'Directory':<{LABEL_WIDTH}} {info['directory']}")

    venv = info["venv"]
    lines.append(f"{'Venv':<{LABEL_WIDTH}} {venv if venv else 'not active'}")
    lines.append(f"{'Interpreter':<{LABEL_WIDTH}} {info['interpreter']}")

    lines.append(f"{'Tempeh':<{LABEL_WIDTH}} {info['tempeh']['version']}")
    lines.append(f"{'Python':<{LABEL_WIDTH}} {info['python']['version']}")

    lines.append("")
    for name in KNOWN_TOOLS:
        tool = info["tools"][name]
        if tool["available"]:
            lines.append(f"{name:<{LABEL_WIDTH}} {tool['version']}")
        elif name in PREFERRED_TOOLS:
            lines.append(f"{name:<{LABEL_WIDTH}} not found")

    return "\n".join(lines)
