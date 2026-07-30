## 1. Fix Due Date Parser

- [x] 1.1 In `src/knbn/widgets/card.py`, replace `_parse_due` to use `parse_datetime` from `knbn.model.task` instead of the legacy `DD/MM/YYYY` strptime

## 2. Add Setting

- [x] 2.1 In `src/knbn/config.py`, add `'deadline_warning_hours': '24'` to `SETTINGS_DEFAULTS`

## 3. Update Card Rendering

- [x] 3.1 In `src/knbn/widgets/card.py`, update `_due_display` (or equivalent) to return a formatted due string using `display_date`-style output (`YYYY-MM-DD` or `YYYY-MM-DD HH:MM`)
- [x] 3.2 Add `_is_deadline_warning` method to `TaskCard` that reads `deadline_warning_hours` from settings and returns `True` if the due date is within that window (or past)
- [x] 3.3 Update `TaskCard.compose` to place the due date right-aligned on the title row, truncating the title to leave room when both are present
- [x] 3.4 Add `.-deadline-warning` CSS class to `TaskCard.DEFAULT_CSS` that sets `border: round $warning`
- [x] 3.5 In `TaskCard.on_mount`, call `add_class('-deadline-warning')` / `remove_class('-deadline-warning')` based on `_is_deadline_warning()`

## 4. Pass Data Directory to Card

- [x] 4.1 Confirm `TaskCard` already receives `data_dir` (it does — used for notes); use it to call `get_setting` in `_is_deadline_warning`

## 5. Verify

- [x] 5.1 Run `uv run pytest tests` — all tests pass
- [x] 5.2 Run `uv run mypy src/` — no type errors
- [ ] 5.3 Launch `uv run knbn board`, confirm a task with a near due date shows the warning border and due date on the title row
