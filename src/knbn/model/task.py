"""Task data model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

_NEW_DATETIME_FMT = '%Y-%m-%d %H:%M'
_NEW_DATE_FMT = '%Y-%m-%d'
_OLD_FMTS = ['%B %d, %Y %I:%M %p', '%B  %d, %Y %I:%M %p']


def now_str() -> str:
    return datetime.now().strftime(_NEW_DATETIME_FMT)


def parse_datetime(s: str) -> tuple[datetime, bool] | None:
    """Parse a date/datetime string in new or legacy format.

    Returns (datetime, has_time) or None if unrecognised.
    """
    if not s:
        return None
    s = s.strip()
    try:
        return datetime.strptime(s, _NEW_DATETIME_FMT), True
    except ValueError:
        pass
    try:
        return datetime.strptime(s, _NEW_DATE_FMT), False
    except ValueError:
        pass
    for fmt in _OLD_FMTS:
        try:
            return datetime.strptime(s, fmt), True
        except ValueError:
            continue
    return None


def display_date_only(s: str) -> str:
    """Return YYYY-MM-DD for a stored date/datetime value, stripping any time component."""
    if not s:
        return ''
    result = parse_datetime(s)
    if result is None:
        return s
    dt, _ = result
    return dt.strftime(_NEW_DATE_FMT)


@dataclass
class Task:
    title: str
    category: str
    status: str
    priority: str
    date_created: str
    date_modified: str
    due: str = field(default='')
    key_resource: str = field(default='')
    free_text_1: str = field(default='')
    free_text_2: str = field(default='')
    free_text_3: str = field(default='')
