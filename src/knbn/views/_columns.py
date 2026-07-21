"""Shared column layout constants and helpers for table views."""

from __future__ import annotations

from knbn.model.task import display_date as _display_date

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


def display_date(s: str) -> str:
    return _display_date(s)
