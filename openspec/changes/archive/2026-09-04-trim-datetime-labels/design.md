## Context

`display_date()` in `src/knbn/model/task.py` currently returns `YYYY-MM-DD HH:MM` when the stored value includes a time component, and `YYYY-MM-DD` otherwise. It is called from `tabular.py` and `done_week.py` before passing values to `format_row()`. The column header is assembled in `_columns.py::header_text()` which hard-codes the string `"Due Date"`.

## Goals / Non-Goals

**Goals:**
- Table views (Tabular, Closed/done_week) always display dates as `YYYY-MM-DD`
- Column header label for the due-date column is `"Due"`

**Non-Goals:**
- Changing how dates are stored; the CSV format is unchanged
- Affecting any view other than TabularView and ClosedView (done_week)
- Modifying the kanban board card or any other date display surface

## Decisions

### Add a `display_date_only()` helper instead of changing `display_date()`

`display_date()` correctly serves callers that want the time shown (e.g., future tooltip or detail views). Changing it globally would be a silent regression risk. Instead, add a small `display_date_only(s: str) -> str` helper that always strips the time, and use it in the two table views.

Alternative considered: add a `show_time: bool = True` parameter to `display_date()`. Rejected — a boolean flag is harder to read at call sites and introduces branching in a function that is already clear.

### Change header string in `_columns.py` directly

The header label `"Due Date"` is a string literal in `header_text()`. Replace with `"Due"`. The `_NON_TITLE_WIDTH` constant and its comment reference "Due Date" width; update both to reflect the shorter label (3 chars saved, header comment updated to `"Due"` header min).

## Risks / Trade-offs

- [Test breakage] Tests asserting the header string `"Due Date"` or time-format output will fail. → Expected; update those tests as part of the same change.
- [display_date_only separate from display_date] Two functions with similar names could confuse future contributors. → Keep both short and well-named; the distinction is clear from the names.
