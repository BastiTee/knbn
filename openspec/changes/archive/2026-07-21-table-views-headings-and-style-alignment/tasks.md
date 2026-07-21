## 1. Shared column format constants

- [x] 1.1 Define the shared column format string (header and data row template) as a module-level constant in `src/knbn/views/_row.py` or a new `src/knbn/views/_columns.py` — `HEADER_TEXT` and a helper `format_row(name, status, priority, category, created, edited, due)` that formats one row string with the fixed widths from the design (Name 28, Status 11, Priority 9, Category 14, Created 16, Edited 16, Due rest)
- [x] 1.2 Add a `_date_only(s: str) -> str` helper that extracts the date portion from a stored datetime string (e.g. `"July 21, 2026 03:45 PM"` → `"July 21, 2026"`); return empty string for empty input

## 2. Tabular view

- [x] 2.1 In `TabularView.compose()`, yield a non-focusable `Static(HEADER_TEXT, classes='col-header-row')` as the very first widget, before any group headers or rows
- [x] 2.2 Rewrite the data row format string in `TabularView.compose()` to use the new column order and widths: Name (28), Status (11), Priority (9), Category (14), Created (16), Edited (16), Due; use `_date_only()` for both date fields
- [x] 2.3 Add CSS for `.col-header-row` in `TabularView.DEFAULT_CSS`: `text-style: bold; padding: 0 1;` (no background, so it blends into the view background)

## 3. Closed view

- [x] 3.1 In `ClosedView.compose()`, yield a non-focusable `Static(HEADER_TEXT, classes='col-header-row')` as the very first widget, before any week headers or rows
- [x] 3.2 Rewrite the data row format string in `ClosedView.compose()` to use the new column order and widths: Name (28), Status (11), Priority (9), Category (14), Created (16), Edited (16), Due; use `_date_only()` for both date fields
- [x] 3.3 In `ClosedView.DEFAULT_CSS`, change `.week-header` background from `$surface-darken-1` to `$primary-darken-2`
- [x] 3.4 Add CSS for `.col-header-row` in `ClosedView.DEFAULT_CSS`: `text-style: bold; padding: 0 1;`

## 4. Verification

- [x] 4.1 Launch the TUI (`uv run knbn board`) and switch to the Tabular view — confirm the header row appears, columns are labelled correctly, and data rows align under the headers
- [x] 4.2 Switch to the Closed view — confirm the header row appears, week headers use the same colour as Tabular group headers, and data rows align under the headers
- [x] 4.3 Run `uv run pytest tests` and confirm all tests pass
- [x] 4.4 Run `uv run mypy src/` and confirm no type errors
