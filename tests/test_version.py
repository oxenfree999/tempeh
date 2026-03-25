import re

from tempeh.version import VERSION


def test_version_is_set():
    assert re.fullmatch(r"\d+\.\d+\.\d+", VERSION)
