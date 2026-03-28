"""Configuration schema and platform directory resolution."""

from dataclasses import dataclass
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

    state_dir: Path | None = None


@dataclass(frozen=True, slots=True)
class PythonConfig:
    """[python] section.

    python_path (Path | None): overrides uv/PATH discovery with an explicit binary. Default: None.
    """

    python_path: Path | None = None


@dataclass(frozen=True, slots=True)
class LaunchConfig:
    """[launch] section.

    mode (str): 'attached' or 'headless'. Default: 'attached'.
    """

    mode: str = "attached"


@dataclass(frozen=True, slots=True)
class ProcessConfig:
    """[process] section.

    stop_timeout (str): duration before suggesting kill (e.g. '10s', '1m'). Default: '10s'.
    stop_signal (str): signal sent by stop — 'SIGTERM', 'SIGINT', etc. Default: 'SIGTERM'.
    """

    stop_timeout: str = "10s"
    stop_signal: str = "SIGTERM"


@dataclass(frozen=True, slots=True)
class SessionConfig:
    """[session] section.

    name_prefix (str): default prefix for auto-generated session names. Default: 'psoul'.
    tags (dict | None): default key-value tags applied to all sessions. Default: None.
    id_format (str): 'short' (human-readable) or 'uuid'. Default: 'short'.
    """

    name_prefix: str = "psoul"
    tags: dict[str, str] | None = None
    id_format: str = "short"


@dataclass(frozen=True, slots=True)
class OutputConfig:
    """[output] section.

    format (str): 'text', 'json', or 'ndjson'. Default: 'text'.
    color (str): 'auto', 'always', or 'never'. Default: 'auto'.
    timestamps (bool): show timestamps in human-readable output. Default: True.
    """

    format: str = "text"
    color: str = "auto"
    timestamps: bool = True


@dataclass(frozen=True, slots=True)
class RetentionConfig:
    """[retention] section.

    max_age (str): auto-prune sessions older than this. Default: '7d'.
    max_sessions (int): max completed sessions to keep. Default: 100.
    max_artifact_mb (int): per-session artifact cap in MB. Default: 500.
    """

    max_age: str = "7d"
    max_sessions: int = 100
    max_artifact_mb: int = 500


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
