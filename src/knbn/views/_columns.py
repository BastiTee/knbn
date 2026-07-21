"""Shared column layout constants and helpers for table views."""

from __future__ import annotations

# Column widths: Name 28, Status 11, Priority 9, Category 14, Created 16, Edited 16, Due rest
HEADER_TEXT = (
    f'  {"Name":<28} {"Status":<11} {"Priority":<9} {"Category":<14}'
    f' {"Created":<16} {"Edited":<16} Due Date'
)


def format_row(
    name: str,
    status: str,
    priority: str,
    category: str,
    created: str,
    edited: str,
    due: str,
) -> str:
    name_col = name if len(name) <= 28 else name[:27] + '…'
    return (
        f'  {name_col:<28} {status:<11} {priority:<9} {category:<14}'
        f' {created:<16} {edited:<16} {due}'
    )


def _date_only(s: str) -> str:
    """Return just the date portion of a stored datetime string.

    "July 21, 2026 03:45 PM" → "July 21, 2026"
    """
    if not s:
        return ''
    # The stored format is "Month DD, YYYY HH:MM AM/PM" — split on space and
    # rejoin the first three tokens (month, day+comma, year).
    parts = s.strip().split()
    if len(parts) >= 3:
        return ' '.join(parts[:3])
    return s
