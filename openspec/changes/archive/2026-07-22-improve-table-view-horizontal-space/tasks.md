## 1. Update column formatter

- [x] 1.1 Add `FIXED_COLS_WIDTH` constant to `_columns.py` (sum of all non-title column widths + padding)
- [x] 1.2 Add `title_width: int` parameter to `format_row()` and update truncation logic to use it
- [x] 1.3 Add `header_text(title_width: int) -> str` function (or update `HEADER_TEXT` to a callable) so header aligns with data rows

## 2. Wire dynamic width into views

- [x] 2.1 Override `on_resize` in `TabularView` to call `self.call_after_refresh(self.recompose)`
- [x] 2.2 Update `TabularView.compose()` to compute `title_width` from `self.size.width` and pass it to `format_row` and the header
- [x] 2.3 Override `on_resize` in `ClosedView` to call `self.call_after_refresh(self.recompose)`
- [x] 2.4 Update `ClosedView.compose()` to compute `title_width` from `self.size.width` and pass it to `format_row` and the header

## 3. Verify and clean up

- [x] 3.1 Run `uv run pytest tests` and confirm no regressions
- [x] 3.2 Run `uv run mypy src/` and fix any type errors
- [x] 3.3 Run `uv run ruff check --fix src/ tests/` and `uv run ruff format src/ tests/`
- [ ] 3.4 Manually launch `uv run knbn board`, switch to tabular and done views, resize the terminal and confirm title column expands
