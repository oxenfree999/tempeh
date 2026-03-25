import pytest
import structlog


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("TERM", raising=False)
    monkeypatch.delenv("TEMPEH_LOG", raising=False)
    monkeypatch.setenv("COLUMNS", "80")
    # Prevent Rich from reducing width by 1 on Windows legacy consoles.
    # Rich's own test suite does the equivalent via legacy_windows=False.
    monkeypatch.setattr("rich.console.WINDOWS", False)


@pytest.fixture(autouse=True)
def _reset_structlog():
    yield
    structlog.reset_defaults()
