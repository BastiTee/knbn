## Why

All date and datetime values in the app currently use the verbose Notion export format (`"July 21, 2026 03:45 PM"`), which is locale-sensitive, uses 12-hour AM/PM time, and is hard to read at a glance. Standardising on ISO-like formats (`YYYY-MM-DD` for date-only, `YYYY-MM-DD HH:MM` for datetime) makes timestamps unambiguous, sortable as plain strings, and familiar to technical users. The form currently accepts a bespoke `DD/MM/YYYY` format for Due with no validation, and `now_str()` writes the old verbose format on every new task and status change.

## What Changes

- Replace `now_str()` return format with `YYYY-MM-DD HH:MM`.
- Add a `parse_datetime(s)` / `format_datetime(dt)` pair in the model to centralise read/write of both the old and new formats (for backwards compatibility when reading existing data).
- In `_columns.py`, replace `_date_only()` with a smarter `display_date(s)` that shows `YYYY-MM-DD HH:MM` if a time is present, or `YYYY-MM-DD` if only a date is present.
- In the task edit form, change the Due label to `YYYY-MM-DD (optional)` and validate the input on save, showing an inline error for any non-conforming value.
- Migrate `tests/fixtures/tasks.csv` to the new format for both `Date Created` and `Last edited time` columns, and normalise `Due` column values.
- Update `_parse_modified()` in `done_week.py` to also recognise the new format so the Closed view groups correctly from day one.

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `task-model`: `now_str()` format changes; new normalisation helpers; datetime format becomes part of the contract.
- `tui-board`: Form validation for Due field; display logic for date vs datetime in table views.

## Impact

- `src/knbn/model/task.py` — `now_str()`, new helpers `parse_datetime()` and `display_date()`.
- `src/knbn/views/_columns.py` — `_date_only()` replaced by `display_date()`.
- `src/knbn/views/done_week.py` — `_parse_modified()` extended to handle new format.
- `src/knbn/widgets/form.py` — Due label update and validation.
- `tests/fixtures/tasks.csv` — migrate all date values to new format.
- Any existing persisted `~/.knbn/tasks.csv` is NOT automatically migrated (out of scope); the reader will handle old format via backwards-compat parsing.
