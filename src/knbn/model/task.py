"""Task data model."""

from __future__ import annotations

from dataclasses import dataclass, field

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
