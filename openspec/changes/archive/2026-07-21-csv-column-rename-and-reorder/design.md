## Context

`store.py` defines `_CSV_FIELDNAMES` with the ten Notion-inherited column names and uses them in `_task_to_row()` and `_row_to_task()`. These are the only places that know about column names — the `Task` dataclass uses its own Python attribute names (`date_created`, `date_modified`, etc.) and is unaffected by CSV column names. The CSV is written by `save_tasks()` / `ensure_data_dir()` and read by `load_tasks()`.

## Goals / Non-Goals

**Goals:**
- Replace the ten column name strings in `_CSV_FIELDNAMES` with the new names in the new order.
- Update the string literals in `_task_to_row()` and `_row_to_task()` accordingly.
- Add a `_validate_csv_schema(path: Path) -> None` function that reads the header row of an existing CSV and raises `ValueError` with a clear message if the columns don't match `_CSV_FIELDNAMES` exactly (order matters, since the order is now canonical).
- Call `_validate_csv_schema` from `load_tasks()` before reading rows, so any launch of the TUI or CLI that touches an existing file will surface schema mismatches immediately.
- Migrate `tests/fixtures/tasks.csv` and `demo/tasks.csv`.
- Fix the single test that asserts the old header string.
- Add a test for the new schema validation error path.

**Non-Goals:**
- An automatic migration tool for existing user `~/.knbn/tasks.csv` files — users with old data need to rename columns manually or re-init. A clear error message from the validator is sufficient.
- Changing any Python attribute names on `Task` — those are already clean.
- Changing any UI labels in the TUI forms or CLI prompts — those use human-readable strings unrelated to CSV column names.

## Decisions

### Validate on `load_tasks`, not `ensure_data_dir`

`ensure_data_dir` only writes a fresh header when the file doesn't yet exist — it never reads an existing file. The right place to catch a mismatch is `load_tasks`, which is called on every app launch and every reload. Raising `ValueError` there means the TUI startup will propagate the error cleanly to the terminal before the UI starts.

**Alternative considered:** Validate inside the TUI `App.on_mount`. Rejected — model code should not depend on TUI code; the store is the layer that owns the schema contract.

### Raise `ValueError` with a descriptive message

The error message includes the actual header found so the user knows what their file has. Format:
```
tasks.csv has wrong schema.
Expected: DateTimeCreated,DateTimeEdited,...
Found:    Name,Category,...
```

**Alternative considered:** Return `False` and let callers decide. Rejected — schema mismatch is always fatal for this app; an exception is the right signal.

### Column order is part of the contract

The validator checks exact order, not just set membership. This keeps the schema unambiguous and makes the CSV human-readable in a consistent way.

## Risks / Trade-offs

- [Risk] Users with existing `~/.knbn/tasks.csv` using the old schema get a hard error on next launch. Mitigation: the error message is descriptive enough for users to understand what happened; the CLAUDE.md documents the schema; no silent data loss occurs.
- [Trade-off] Order-sensitive validation is stricter than needed for correctness (CSV readers by name don't care about order). Accepted — the canonical order is a design goal, not just a parser requirement.
