"""Task data model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

STATUS_ACTIVE: list[str] = ['Todo', 'Now', 'Feedback']
STATUS_TERMINAL: list[str] = ['Done', 'Delegated', 'Stopped']
STATUS_VALUES: list[str] = STATUS_ACTIVE + STATUS_TERMINAL

PRIORITY_VALUES: list[str] = ['High', 'Medium', 'Low']

DEFAULT_CATEGORIES: list[str] = [
    'People',
    'Hiring',
    'Strategy',
    'Product',
    'Engineering',
    'Work Life',
    'Ideas',
]

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


def display_date(s: str) -> str:
    """Return a display string for a stored date/datetime value.

    Shows YYYY-MM-DD HH:MM when a time component is present,
    YYYY-MM-DD when only a date is stored. Returns '' for empty input.
    """
    if not s:
        return ''
    result = parse_datetime(s)
    if result is None:
        return s
    dt, has_time = result
    if has_time:
        return dt.strftime(_NEW_DATETIME_FMT)
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
    feedback_from: str = field(default='')
    delegated_to: str = field(default='')
