## Why

Table views show datetime values like `2024-03-15 09:30` in the Created, Edited, and Due columns, but the time portion adds noise with no value at this granularity — users care about the date, not the hour. The column header "Due Date" is also inconsistent with the shorter "Created" and "Edited" labels.

## What Changes

- `display_date()` in table views always renders only the date portion (`YYYY-MM-DD`), stripping the time component even when a time is stored
- Column header `Due Date` → `Due` in `_columns.py`
- `_NON_TITLE_WIDTH` and related comment updated to reflect the narrower "Due" header

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `responsive-table-columns`: column header label changes from "Due Date" to "Due"; the date format in Created, Edited, and Due columns changes from `YYYY-MM-DD HH:MM` (when time present) to always `YYYY-MM-DD`

## Impact

- `src/knbn/views/_columns.py` — header label and `_NON_TITLE_WIDTH` constant
- `src/knbn/model/task.py` — `display_date()` or a new date-only helper used by table views
- `src/knbn/views/tabular.py` and `src/knbn/views/done_week.py` — call sites that pass date strings to `format_row`
- Tests covering `display_date` or column header text may need updating
