import pytest
import structlog


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("TERM", raising=False)
    monkeypatch.delenv("TEMPEH_LOG", raising=False)
    monkeypatch.setenv("COLUMNS", "80")


@pytest.fixture(autouse=True)
def _reset_structlog():
    yield
    structlog.reset_defaults()
