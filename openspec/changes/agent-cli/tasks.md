## 1. Dependencies and Task model

- [x] 1.1 Add `filelock` to `[project.dependencies]` in `pyproject.toml` and verify `uv sync` completes without error
- [x] 1.2 Add `id: str = ""` field to the `Task` dataclass in `src/knbn/model/task.py` and verify existing `Task` construction tests still pass with no changes
- [x] 1.3 Add `generate_id() -> str` function in `src/knbn/model/task.py` (8-char lowercase hex via `secrets.token_hex(4)`) and verify format and uniqueness with a unit test generating 1000 IDs

## 2. Store schema migration

- [x] 2.1 Add `ID` as the first element of `_CSV_FIELDNAMES` in `src/knbn/model/store.py` and update `_task_to_row` / `_row_to_task` to include the `ID` column; verify that `save_tasks` + `load_tasks` round-trip preserves the `id` field
- [x] 2.2 Update `_validate_csv_schema` to accept the old 11-column header (returning tasks with `id=""` for all rows) and the new 12-column header; anything else still raises `ValueError`; verify both branches with unit tests
- [x] 2.3 Add `_ensure_ids(tasks: list[Task], existing_ids: set[str]) -> list[Task]` helper that assigns a fresh unique ID to any task where `id` is empty string, retrying on collision; verify via unit test that after the call all tasks have non-empty, distinct IDs

## 3. Store locking and ID-based CRUD

- [x] 3.1 Wrap `save_tasks` in a `filelock.FileLock` on `tasks.csv.lock` with a 10-second timeout; call `_ensure_ids` before writing; raise `StoreLockedError` (new `ValueError` subclass) on timeout; verify that `StoreLockedError` is raised in a test that holds the lock and calls `save_tasks` from a second thread
- [x] 3.2 Add `TaskNotFoundError` (subclass of `ValueError`) to `src/knbn/model/store.py`
- [x] 3.3 Add `find_task_by_id(data_dir, task_id) -> Task` that raises `TaskNotFoundError` for unknown IDs; verify with unit tests for both found and not-found cases
- [x] 3.4 Add `update_task_by_id(data_dir, task_id, task)` that raises `TaskNotFoundError` for unknown IDs; verify with a unit test
- [x] 3.5 Add `delete_task_by_id(data_dir, task_id)` that raises `TaskNotFoundError` for unknown IDs and also removes the notes file; verify with unit tests for both cases (with and without notes file)

## 4. db_version in settings

- [x] 4.1 Update `ensure_data_dir` in `src/knbn/model/store.py` to write `db_version` (from `importlib.metadata.version("knbn")`) as a top-level key in `settings.json` after initialization; verify the key is present after calling `ensure_data_dir` on a fresh directory
- [x] 4.2 Call `save_settings` with the updated `db_version` inside `save_tasks` after a migration (i.e., when `_ensure_ids` actually assigned new IDs to previously empty rows); verify with a unit test that migrating an old CSV also updates `db_version`

## 5. Test fixtures update

- [x] 5.1 Add the `ID` column (first column) to `tests/fixtures/tasks.csv` with pre-generated 8-char IDs for all 16 rows; verify that `load_tasks` parses the fixture without error and that all returned tasks have non-empty `id` fields

## 6. knbn add — JSON flag

- [x] 6.1 Add `--json` flag to `knbn add` in `src/knbn/cli.py`; when set, print `task_to_dict(task)` as JSON to stdout instead of the confirmation string; verify that `knbn add --fast --title "T" --json` outputs valid JSON with a non-empty `id` field and that the human-readable output is unchanged without the flag

## 7. knbn list

- [x] 7.1 Implement `task_to_dict(task: Task) -> dict` serializer in a shared location (e.g. `src/knbn/cli.py` or a new `src/knbn/model/serial.py`); verify that all 12 fields are present in the output dict with snake_case keys
- [x] 7.2 Implement `knbn list` in `src/knbn/cli.py` with default human-readable tabular output (ID, Status, Priority, Category, Title columns) sorted by status order → priority → title; verify with a CLI test against the fixture
- [x] 7.3 Add `--status`, `--priority`, `--category` repeatable filter flags to `knbn list` with AND-across-flags, OR-within-repeated-flag semantics; verify combined and single-flag filtering
- [x] 7.4 Add `--all` flag to `knbn list` that includes terminal-status tasks; verify that without `--all` only active tasks appear and with `--all` all tasks appear
- [x] 7.5 Add `--json` flag to `knbn list`; verify output is a valid JSON array, respects filters, and returns `[]` when no tasks match

## 8. knbn edit

- [x] 8.1 Implement `knbn edit <id>` in `src/knbn/cli.py` with all editable-field flags (`--title`, `--status`, `--priority`, `--category`, `--due`, `--key-resource`, `--free-text-1`, `--free-text-2`, `--free-text-3`); verify at least one flag is required or exit non-zero
- [x] 8.2 Add validation for `--status`, `--priority`, `--category` against board config values; print valid options on invalid input and exit non-zero; verify with a test using an invalid value
- [x] 8.3 Add `--json` flag to `knbn edit`; verify output is the updated task as a JSON object
- [x] 8.4 Verify that `knbn edit <unknown-id>` exits non-zero with a message containing the unknown ID

## 9. knbn delete

- [x] 9.1 Implement `knbn delete <id>` in `src/knbn/cli.py` with a default confirmation prompt; add `--yes` / `-y` flag to skip it; verify that without `--yes` answering `n` aborts with exit code 0 and no CSV change
- [x] 9.2 Verify that `knbn delete <known-id> --yes` removes the task from the CSV and deletes any associated notes file
- [x] 9.3 Verify that `knbn delete <unknown-id> --yes` exits non-zero with an error message containing the unknown ID

## 10. knbn config

- [x] 10.1 Implement `knbn config` in `src/knbn/cli.py`; verify output is valid JSON containing all required keys (`active_statuses`, `default_active_status`, `terminal_statuses`, `default_terminal_status`, `priorities`, `categories`, `free_text_fields`, `data_dir`) and that repeated calls do not mutate `settings.json`

## 11. Data directory README

- [x] 11.1 Write `src/knbn/defaults/README.md` template covering: what knbn is, all twelve task fields with one-line descriptions, the five core CLI commands (`add`, `list`, `edit`, `delete`, `config`) with example invocations, a note about `settings.json` / `knbn config`, and a note that users can edit the file to add agent-visible context
- [x] 11.2 Update `ensure_data_dir` in `src/knbn/model/store.py` to copy the bundled template to `<data_dir>/README.md` using `importlib.resources` (write only if the file does not already exist); verify with a unit test that a fresh init creates the file and a second call leaves an existing file unchanged

## 12. Final verification

- [x] 12.1 Run `make build` (full chain: tests + mypy + lint + format) and confirm it passes with no new type errors or lint violations
- [x] 12.2 Run `knbn add --fast --title "Agent task" --json | jq .id` and verify a non-empty 8-char ID is printed; then run `knbn list --json | jq length` and verify the count increased
- [x] 12.3 Cat `~/.knbn/README.md` and verify it contains all twelve field names and the five CLI command names
