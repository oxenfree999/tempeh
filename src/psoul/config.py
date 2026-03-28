"""Configuration schema, platform directory resolution, and config generation."""

import dataclasses
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from platformdirs import user_config_path, user_state_path

APP_NAME = "psoul"


def default_config_dir() -> Path:
    """Return the platform-specific user config directory for psoul."""
    return user_config_path(APP_NAME)


def default_state_dir() -> Path:
    """Return the platform-specific user state directory for psoul."""
    return user_state_path(APP_NAME)


@dataclass(frozen=True, slots=True)
class PathsConfig:
    """[paths] section.

    state_dir (Path | None): overrides the default platform state directory. Default: None.
    """

    state_dir: Path | None = field(default=None, metadata={"description": "override session/state directory"})


@dataclass(frozen=True, slots=True)
class PythonConfig:
    """[python] section.

    python_path (Path | None): overrides uv/PATH discovery with an explicit binary. Default: None.
    """

    python_path: Path | None = field(
        default=None, metadata={"description": "override Python binary, bypasses uv discovery"}
    )


@dataclass(frozen=True, slots=True)
class LaunchConfig:
    """[launch] section.

    mode (str): 'attached' or 'headless'. Default: 'attached'.
    """

    mode: str = field(default="attached", metadata={"description": "attached (default) or headless"})


@dataclass(frozen=True, slots=True)
class ProcessConfig:
    """[process] section.

    stop_timeout (str): duration before suggesting kill (e.g. '10s', '1m'). Default: '10s'.
    stop_signal (str): signal sent by stop — 'SIGTERM', 'SIGINT', etc. Default: 'SIGTERM'.
    """

    stop_timeout: str = field(default="10s", metadata={"description": "how long stop waits before suggesting kill"})
    stop_signal: str = field(default="SIGTERM", metadata={"description": "signal sent by stop (SIGTERM, SIGINT, etc.)"})


@dataclass(frozen=True, slots=True)
class SessionConfig:
    """[session] section.

    name_prefix (str): default prefix for auto-generated session names. Default: 'psoul'.
    tags (dict | None): default key-value tags applied to all sessions. Default: None.
    id_format (str): 'short' (human-readable) or 'uuid'. Default: 'short'.
    """

    name_prefix: str = field(default="psoul", metadata={"description": "default name prefix for unnamed sessions"})
    tags: dict[str, str] | None = field(
        default=None, metadata={"description": "default key-value tags applied to all sessions"}
    )
    id_format: str = field(default="short", metadata={"description": "short (human-readable) or uuid"})


@dataclass(frozen=True, slots=True)
class OutputConfig:
    """[output] section.

    format (str): 'text', 'json', or 'ndjson'. Default: 'text'.
    color (str): 'auto', 'always', or 'never'. Default: 'auto'.
    timestamps (bool): show timestamps in human-readable output. Default: True.
    """

    format: str = field(default="text", metadata={"description": "text (default), json, or ndjson"})
    color: str = field(default="auto", metadata={"description": "auto, always, or never"})
    timestamps: bool = field(default=True, metadata={"description": "show timestamps in human-readable output"})


@dataclass(frozen=True, slots=True)
class RetentionConfig:
    """[retention] section.

    max_age (str): auto-prune sessions older than this. Default: '7d'.
    max_sessions (int): max completed sessions to keep. Default: 100.
    max_artifact_mb (int): per-session artifact cap in MB. Default: 500.
    """

    max_age: str = field(default="7d", metadata={"description": "auto-prune sessions older than this"})
    max_sessions: int = field(default=100, metadata={"description": "max completed sessions to keep"})
    max_artifact_mb: int = field(default=500, metadata={"description": "per-session artifact cap in MB"})


@dataclass(frozen=True, slots=True)
class PsoulConfig:
    """Top-level configuration, composed from TOML sections.

    paths (PathsConfig): [paths] section.
    python (PythonConfig): [python] section.
    launch (LaunchConfig): [launch] section.
    process (ProcessConfig): [process] section.
    session (SessionConfig): [session] section.
    output (OutputConfig): [output] section.
    retention (RetentionConfig): [retention] section.
    """

    paths: PathsConfig = PathsConfig()
    python: PythonConfig = PythonConfig()
    launch: LaunchConfig = LaunchConfig()
    process: ProcessConfig = ProcessConfig()
    session: SessionConfig = SessionConfig()
    output: OutputConfig = OutputConfig()
    retention: RetentionConfig = RetentionConfig()


def find_config_file(override: Path | None = None) -> Path | None:
    """Discover the config file to use, following precedence order.

    override (Path | None): explicit --config flag. Raises FileNotFoundError if set but missing.

    Returns the first existing config file, or None if no config found.
    """
    if override is not None:
        if not override.is_file():
            msg = f"Config file not found: {override}"
            raise FileNotFoundError(msg)
        return override

    # Project-local: psoul.toml wins over pyproject.toml
    psoul_toml = Path("psoul.toml")
    if psoul_toml.is_file():
        return psoul_toml

    pyproject = Path("pyproject.toml")
    if pyproject.is_file():
        with pyproject.open("rb") as f:
            data = tomllib.load(f)
        if "psoul" in data.get("tool", {}):
            return pyproject

    # User-level config
    user_config = default_config_dir() / "config.toml"
    if user_config.is_file():
        return user_config

    return None


def _extract_psoul_table(path: Path, data: dict) -> dict:
    """Extract the psoul config table from raw TOML data.

    For pyproject.toml, reads from [tool.psoul]. For other files, returns data as-is.
    """
    if path.name == "pyproject.toml":
        return data.get("tool", {}).get("psoul", {})
    return data


def load_config(path: Path | None = None) -> PsoulConfig:
    """Load configuration from a TOML file into a PsoulConfig.

    path (Path | None): file path from find_config_file(). None means all defaults.
    """
    if path is None:
        return PsoulConfig()

    with path.open("rb") as f:
        data = tomllib.load(f)

    raw = _extract_psoul_table(path, data)

    return PsoulConfig(
        paths=PathsConfig(**raw.get("paths", {})),
        python=PythonConfig(**raw.get("python", {})),
        launch=LaunchConfig(**raw.get("launch", {})),
        process=ProcessConfig(**raw.get("process", {})),
        session=SessionConfig(**raw.get("session", {})),
        output=OutputConfig(**raw.get("output", {})),
        retention=RetentionConfig(**raw.get("retention", {})),
    )


def _format_toml_value(value: object) -> str:
    """Format a Python value as a TOML literal."""
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def generate_config() -> str:
    """Generate a commented psoul.toml by introspecting PsoulConfig fields.

    Every value is commented out so the file uses all defaults.
    Descriptions come from field metadata, not a separate data structure.
    """
    defaults = PsoulConfig()
    lines = ["# psoul configuration", ""]

    for section_field in dataclasses.fields(defaults):
        section = getattr(defaults, section_field.name)
        lines.append(f"[{section_field.name}]")
        for f in dataclasses.fields(section):
            desc = f.metadata.get("description", "")
            value = getattr(section, f.name)
            comment = f"  # {desc}" if desc else ""
            lines.append(f"# {f.name} = {_format_toml_value(value)}{comment}")
        lines.append("")

    return "\n".join(lines)
