## Why

The tabular and done-week views use fixed column widths that leave significant horizontal space unused on typical terminal widths (≥80 columns). The title column is capped at 28 characters regardless of available space, so longer task names are needlessly truncated.

## What Changes

- The title column in both table views expands dynamically to fill all space not consumed by the fixed-width columns (status, priority, category, created, edited, due date).
- The column layout helper in `src/knbn/views/_columns.py` is updated to accept a terminal width and compute the title column width accordingly.
- `TaskRow` widgets query the available width at render time and pass it to the formatter.

## Capabilities

### New Capabilities

- `responsive-table-columns`: Title column in table views expands to fill available horizontal space instead of being capped at a fixed 28-character width.

### Modified Capabilities

<!-- No existing spec-level requirements are changing — this is a pure UI improvement with no model or CLI behaviour changes. -->

## Impact

- `src/knbn/views/_columns.py` — `format_row` and `HEADER_TEXT` gain a `title_width` parameter.
- `src/knbn/views/tabular.py` and `src/knbn/views/done_week.py` — pass `self.size.width` (or a reactive equivalent) when calling `format_row`.
- No data model, CLI, or storage changes.
