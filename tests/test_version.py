import re

from psoul.version import VERSION


def test_version_is_set() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", VERSION)
