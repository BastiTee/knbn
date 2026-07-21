## Why

The current CSV column names are inherited from Notion's export format (`Name`, `Date Created`, `Last edited time`, etc.) and no longer reflect the project's own conventions. The new names are shorter, camelCase, unambiguous, and consistent with the standardised datetime format introduced in the previous change. The column order is also being rationalised to put the most-queried fields first. This is also an opportunity to add a startup schema validation that catches version mismatches before they silently corrupt data.

## What Changes

- Rename all ten CSV column headers to the new names:
  - `Name` → `Name` (unchanged)
  - `Category` → `Category` (unchanged)
  - `Date Created` → `DateTimeCreated`
  - `Delegated To` → `Delegate`
  - `Due` → `DateTimeDue`
  - `Feedback From` → `Feedback`
  - `Key Resource` → `KeyResource`
  - `Last edited time` → `DateTimeEdited`
  - `Priority` → `Priority` (unchanged)
  - `Status` → `Status` (unchanged)
- Reorder columns to: `DateTimeCreated`, `DateTimeEdited`, `DateTimeDue`, `Status`, `Priority`, `Category`, `Name`, `Delegate`, `Feedback`, `KeyResource`
- Update all read/write code in `store.py` to use the new column names.
- Add a startup schema check in `ensure_data_dir` (and/or `load_tasks`) that validates the CSV header against the expected columns and raises a clear error if they do not match.
- Migrate `tests/fixtures/tasks.csv` and `demo/tasks.csv` to the new schema.
- Update all tests that reference old column names.

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `task-store`: CSV schema (column names, order) and schema validation at startup are changing.

## Impact

- `src/knbn/model/store.py` — `_CSV_FIELDNAMES`, `_task_to_row()`, `_row_to_task()`, new `_validate_csv_schema()` called from `load_tasks()`.
- `tests/fixtures/tasks.csv` — header and column order migrated.
- `demo/tasks.csv` — header and column order migrated.
- `tests/test_store.py` — update header assertion in `test_csv_has_header_after_init`; add schema validation test.
