## Why

Agents increasingly use `knbn` to track their own tasks, letting users observe multi-step agent workflows on the board. The current CLI (`knbn add`) is the only headless interface; agents have no way to list existing tasks, update them, or delete them, and there is no stable per-task identifier that survives reorders or edits.

## What Changes

- **NEW** Task ID field — a short unique identifier stored in every task row; IDs are generated on first write for legacy rows (backward-compatible migration).
- **NEW** `db_version` key in `settings.json` tracks the knbn version that last mutated storage, enabling future migrations.
- **NEW** `knbn list` subcommand — query tasks with optional filters; supports `--json` for machine-readable output.
- **NEW** `knbn edit <id>` subcommand — update one or more fields on an existing task non-interactively via flags.
- **NEW** `knbn delete <id>` subcommand — remove a task and its notes file.
- **NEW** `knbn config` subcommand — print the resolved board configuration (statuses, priorities, categories, free-text field labels) as JSON; read-only.
- **CHANGED** `knbn add` gains `--json` flag to emit the created task (including its new ID) as JSON instead of the human-readable confirmation line.
- **CHANGED** CSV schema gains a new `ID` column; existing CSVs are migrated on first write by assigning IDs to all rows that lack one.
- **CHANGED** Store mutations acquire an advisory file lock before load+save to prevent clobbering under concurrent writers.
- **NEW** `README.md` written to the data directory on init — boilerplate that explains knbn's CLI, data layout, and task fields so agents can discover how to interact with the store by reading the directory. Users can freely edit it, like a `CLAUDE.md`.

## Capabilities

### New Capabilities

- `task-id`: Unique identifier assigned to every task; generation, storage in CSV, and backward-compatible migration of legacy rows.
- `cli-list`: `knbn list` command — filters, ordering, and `--json` output.
- `cli-edit`: `knbn edit <id>` command — non-interactive field updates via flags.
- `cli-delete`: `knbn delete <id>` command — task and notes removal.
- `cli-config`: `knbn config` command — read-only JSON dump of board configuration.
- `store-locking`: Advisory file lock around all store mutations for concurrent-writer safety.
- `db-version`: `db_version` key in `settings.json` recording the last knbn version that mutated the store.
- `data-dir-readme`: Boilerplate `README.md` written to the data directory on init; agent-readable, user-editable.

### Modified Capabilities

- `task-model`: Task dataclass gains an `id` field (optional, defaults to empty string for backward compatibility).
- `task-store`: CSV schema changes (new `ID` column), validation updated, migration logic added, CRUD signatures updated to work with ID-based lookup in addition to index.
- `cli-add`: Gains `--json` flag that emits the created task as JSON and prints the task ID.

## Impact

- `src/knbn/model/task.py` — add `id` field to `Task` dataclass.
- `src/knbn/model/store.py` — add `ID` to `_CSV_FIELDNAMES`, migration logic, file locking, `find_task_by_id`, updated `_row_to_task` / `_task_to_row`.
- `src/knbn/cli.py` — add `list`, `edit`, `delete`, `config` subcommands; extend `add` with `--json`.
- `src/knbn/config.py` — write `db_version` on storage init and migration.
- `src/knbn/defaults/settings.json` — no change (db_version is written dynamically).
- `tests/fixtures/tasks.csv` — update canonical fixture with `ID` column.
- New dependency: `filelock` (or stdlib `fcntl` on POSIX) for advisory locking — prefer `filelock` for cross-platform portability.
- `src/knbn/defaults/README.md` — bundled template written to the data directory on `ensure_data_dir`; not overwritten if the user has already modified it.
