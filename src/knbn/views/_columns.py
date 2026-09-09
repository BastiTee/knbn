"""Shared column layout constants and helpers for table views."""

from __future__ import annotations

# Non-title column widths in format_row / header_text:
# 2 (indent) + 1 + 11 (status) + 1 + 9 (priority) + 1 + 14 (category)
# + 1 + 16 (created) + 1 + 16 (edited) + 1 + 10 (due, YYYY-MM-DD) = 84
_NON_TITLE_WIDTH = 84

# CSS padding consumed per row: view padding:0 1 (2) + TaskRow padding:0 2 (4).
_PADDING_OVERHEAD = 6

# Combined overhead used to derive a responsive title column width.
_FIXED_OVERHEAD = _NON_TITLE_WIDTH + _PADDING_OVERHEAD  # 90

_MIN_TITLE_WIDTH = 0


def title_col_width(widget_width: int) -> int:
    """Return the title column width that fills available space."""
    return max(_MIN_TITLE_WIDTH, widget_width - _FIXED_OVERHEAD)


def header_text(title_width: int) -> str:
    return (
        f'  {"Name":<{title_width}} {"Status":<11} {"Priority":<9} {"Category":<14}'
        f' {"Created":<16} {"Edited":<16} Due'
    )


def format_row(
    name: str,
    status: str,
    priority: str,
    category: str,
    created: str,
    edited: str,
    due: str,
    title_width: int,
) -> str:
    name_col = name if len(name) <= title_width else name[: title_width - 1] + '…'
    return (
        f'  {name_col:<{title_width}} {status:<11} {priority:<9} {category:<14}'
        f' {created:<16} {edited:<16} {due}'
    )
