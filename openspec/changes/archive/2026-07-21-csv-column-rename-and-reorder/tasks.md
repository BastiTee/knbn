## 1. Update store.py

- [x] 1.1 Replace `_CSV_FIELDNAMES` in `src/knbn/model/store.py` with the new names in the new order: `['DateTimeCreated', 'DateTimeEdited', 'DateTimeDue', 'Status', 'Priority', 'Category', 'Name', 'Delegate', 'Feedback', 'KeyResource']`
- [x] 1.2 Update `_task_to_row()` to use the new column names as dict keys
- [x] 1.3 Update `_row_to_task()` to read from the new column names (use `row['Name']`, `row['DateTimeCreated']`, `row['DateTimeEdited']`, `row.get('DateTimeDue', '')`, `row.get('KeyResource', '')`, `row.get('Feedback', '')`, `row.get('Delegate', '')`)
- [x] 1.4 Add `_validate_csv_schema(path: Path) -> None` that opens the file, reads just the header row via `csv.reader`, and raises `ValueError` if the columns don't match `_CSV_FIELDNAMES` exactly; include both expected and found header in the message
- [x] 1.5 Call `_validate_csv_schema(csv_file)` at the top of `load_tasks()`, before the DictReader loop, only when the file exists

## 2. Migrate data files

- [x] 2.1 Rewrite `tests/fixtures/tasks.csv` header and column order to match the new schema; reorder all data rows accordingly
- [x] 2.2 Rewrite `demo/tasks.csv` header and column order to match the new schema; reorder all data rows accordingly

## 3. Update tests

- [x] 3.1 In `tests/test_store.py`, update `test_csv_has_header_after_init` to assert the new header string `DateTimeCreated,DateTimeEdited,...`
- [x] 3.2 Add `test_load_tasks_wrong_schema` that writes a CSV with the old header to a tmp dir and asserts that `load_tasks` raises `ValueError` containing the expected and found headers

## 4. Verification

- [x] 4.1 Run `uv run pytest tests` and confirm all tests pass
- [x] 4.2 Run `uv run mypy src/` and confirm no type errors
