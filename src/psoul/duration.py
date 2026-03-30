"""Parse human-readable duration strings like '10s' or '1h30m' into timedelta."""

import re
from datetime import timedelta

_UNITS = {
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
}

_PATTERN = re.compile(r"(\d+\.?\d*)([smhdw])")


def parse_duration(s: str) -> timedelta:
    """Convert a duration string like '10s' or '1h30m' into a timedelta."""
    matches = _PATTERN.findall(s)
    if not matches:
        msg = f"invalid duration: {s!r}"
        raise ValueError(msg)
    kwargs = {_UNITS[unit]: float(value) for value, unit in matches}
    return timedelta(**kwargs)
