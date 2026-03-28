"""Tests for configuration schema and platform directory resolution."""

from pathlib import Path

import pytest

from psoul.config import (
    LaunchConfig,
    OutputConfig,
    PathsConfig,
    ProcessConfig,
    PsoulConfig,
    PythonConfig,
    RetentionConfig,
    SessionConfig,
    default_config_dir,
    default_state_dir,
)


def test_default_config_dir_returns_path() -> None:
    result = default_config_dir()
    assert isinstance(result, Path)
    assert "psoul" in result.parts


def test_default_state_dir_returns_path() -> None:
    result = default_state_dir()
    assert isinstance(result, Path)
    assert "psoul" in result.parts


def test_paths_config_defaults() -> None:
    config = PathsConfig()
    assert config.state_dir is None


def test_python_config_defaults() -> None:
    config = PythonConfig()
    assert config.python_path is None


def test_launch_config_defaults() -> None:
    config = LaunchConfig()
    assert config.mode == "attached"


def test_process_config_defaults() -> None:
    config = ProcessConfig()
    assert config.stop_timeout == "10s"
    assert config.stop_signal == "SIGTERM"


def test_session_config_defaults() -> None:
    config = SessionConfig()
    assert config.name_prefix == "psoul"
    assert config.tags is None
    assert config.id_format == "short"


def test_output_config_defaults() -> None:
    config = OutputConfig()
    assert config.format == "text"
    assert config.color == "auto"
    assert config.timestamps is True


def test_retention_config_defaults() -> None:
    config = RetentionConfig()
    assert config.max_age == "7d"
    assert config.max_sessions == 100
    assert config.max_artifact_mb == 500


def test_psoul_config_defaults() -> None:
    config = PsoulConfig()
    assert config.paths.state_dir is None
    assert config.python.python_path is None
    assert config.launch.mode == "attached"
    assert config.process.stop_timeout == "10s"
    assert config.session.name_prefix == "psoul"
    assert config.output.format == "text"
    assert config.retention.max_age == "7d"


def test_psoul_config_override() -> None:
    config = PsoulConfig(
        paths=PathsConfig(state_dir=Path("/tmp/psoul")),
        launch=LaunchConfig(mode="headless"),
    )
    assert config.paths.state_dir == Path("/tmp/psoul")
    assert config.launch.mode == "headless"
    assert config.python.python_path is None  # untouched


def test_config_is_frozen() -> None:
    config = PsoulConfig()
    with pytest.raises(AttributeError):
        config.paths = PathsConfig(state_dir=Path("/tmp"))  # ty: ignore[invalid-assignment]
