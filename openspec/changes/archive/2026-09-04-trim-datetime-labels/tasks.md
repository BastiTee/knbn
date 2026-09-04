## 1. Model helper

- [x] 1.1 Add `display_date_only(s: str) -> str` to `src/knbn/model/task.py` that calls `parse_datetime` and returns only the `YYYY-MM-DD` portion; verify `uv run pytest tests/test_task.py` (or equivalent model tests) passes with new coverage for date-only and datetime inputs

## 2. Column header and layout constant

- [x] 2.1 In `src/knbn/views/_columns.py`, change header label `"Due Date"` → `"Due"` in `header_text()` and update the `_NON_TITLE_WIDTH` comment to reflect the shorter label; verify `uv run pytest tests/` passes and any test asserting the header string is updated

## 3. Table view call sites

- [x] 3.1 In `src/knbn/views/tabular.py`, replace calls to `display_date(...)` with `display_date_only(...)` for created, edited, and due values; verify the import is updated and `uv run pytest tests/` passes

- [x] 3.2 In `src/knbn/views/done_week.py`, replace calls to `display_date(...)` with `display_date_only(...)` for created, edited, and due values; verify the import is updated and `uv run pytest tests/` passes

## 4. Final check

- [x] 4.1 Run `make build` (test + mypy + lint + format) and confirm it exits clean
