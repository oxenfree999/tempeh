from collections.abc import Iterator

import pytest
import structlog


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("TERM", raising=False)
    monkeypatch.delenv("PSOUL_LOG", raising=False)
    monkeypatch.setenv("COLUMNS", "80")
    # Prevent Rich from reducing width by 1 on Windows legacy consoles.
    # Rich's own test suite does the equivalent via legacy_windows=False.
    monkeypatch.setattr("rich.console.WINDOWS", False)


@pytest.fixture(autouse=True)
def _reset_structlog() -> Iterator[None]:
    yield
    structlog.reset_defaults()
