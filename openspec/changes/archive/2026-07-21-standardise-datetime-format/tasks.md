## 1. Model helpers (task.py)

- [x] 1.1 Change `now_str()` to return `datetime.now().strftime('%Y-%m-%d %H:%M')`
- [x] 1.2 Add `parse_datetime(s: str) -> tuple[datetime, bool] | None` that tries formats in order: `%Y-%m-%d %H:%M` (has_time=True), `%Y-%m-%d` (has_time=False), `%B %d, %Y %I:%M %p` (has_time=True), `%B  %d, %Y %I:%M %p` (has_time=True); returns `None` on no match
- [x] 1.3 Add `display_date(s: str) -> str` that calls `parse_datetime`, returns `YYYY-MM-DD HH:MM` if has_time else `YYYY-MM-DD`; returns empty string for empty input

## 2. Update _columns.py

- [x] 2.1 Replace the `_date_only` import and implementation with `display_date` imported from `knbn.model.task`; update all call sites in `format_row` usage

## 3. Update done_week.py

- [x] 3.1 Remove the local `_parse_modified` function and replace it with `parse_datetime` imported from `knbn.model.task`; update call sites to unpack the `(datetime, has_time)` tuple (only the `datetime` part is needed for week grouping)

## 4. Update form.py

- [x] 4.1 Change the Due field label from `'Due (DD/MM/YYYY, optional)'` to `'Due (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional)'`
- [x] 4.2 Add an `id='due-error'` `Static('')` widget below the Due `Input` in `compose()`; add CSS rule `.due-error { color: $error; height: auto; }` to `DEFAULT_CSS`
- [x] 4.3 In `_save()`, before saving validate the Due field value against the regex `^(\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?)?$`; if invalid, set the `due-error` Static content to `'Invalid format — use YYYY-MM-DD or YYYY-MM-DD HH:MM'` and return without saving; if valid, clear the error

## 5. Migrate test fixture

- [x] 5.1 Rewrite `tests/fixtures/tasks.csv`: convert all `Date Created` values from `"Month D, YYYY H:MM AM/PM"` to `YYYY-MM-DD HH:MM`; do the same for all `Last edited time` values
- [x] 5.2 Convert `Due` column values from `DD/MM/YYYY HH:MM (TZ)` format to `YYYY-MM-DD HH:MM` (drop timezone suffix, preserve date and time)

## 6. Update tests

- [x] 6.1 Run `uv run pytest tests` — fix any test that relied on the old `now_str()` format or the old fixture date strings
- [x] 6.2 Add tests for `parse_datetime` covering: new datetime format, new date-only format, old verbose format, empty string, unrecognised input
- [x] 6.3 Add tests for `display_date` covering: datetime input, date-only input, legacy format input, empty string

## 7. Verification

- [x] 7.1 Run `uv run pytest tests` and confirm all tests pass
- [x] 7.2 Run `uv run mypy src/` and confirm no type errors
