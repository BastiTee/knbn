## Context

See `proposal.md` for motivation. The current store is a single-writer CSV with an 11-column schema and index-based CRUD. The CLI has three subcommands (`init`, `board`, `add`). Tasks have no stable identifier beyond their row index, which changes on every delete.

The key constraints are:
- CSV column order is canonical (Notion export compatibility).
- The TUI reads tasks via `load_tasks` and writes via `update_task`/`delete_task` by index. These paths must keep working.
- All test fixtures reference the existing 11-column schema.

## Goals / Non-Goals

**Goals:**
- Stable per-task IDs for script/agent use.
- Four new CLI subcommands (`list`, `edit`, `delete`, `config`).
- `--json` output on `add` and the new subcommands.
- Exclusive write-locking to serialize concurrent mutations.
- `db_version` in `settings.json` for migration tracking.

**Non-Goals:**
- Changing the TUI or any widget code.
- A full migration wizard or user-visible migration prompt.
- Removing the index-based internal helpers immediately (they are used by the TUI; deprecate but keep).

## Decisions

### ID format: 8-char base36 (lowercase alphanumeric)
`secrets.token_hex(4)` yields 8 hex chars, which is 32 bits — roughly 1-in-4-billion collision probability for any two tasks. Lowercase hex satisfies the URL-safe alphanumeric constraint without an extra dependency. Uniqueness is enforced by checking against the existing ID set in `save_tasks` before writing.

**Alternative considered**: UUID4 — too long and verbose for a terminal display column; adds no meaningful collision protection given the expected scale.

### New CSV column position: first (`ID` as column 0)
Placing `ID` first makes it the natural left-most column in any tabular display and is easy for humans and tools to read. Backward-compatible migration: existing rows get an empty `ID` on first schema-mismatch read; they receive fresh IDs on first write.

**Alternative considered**: Last column — avoids changing column indices used by the TUI, but the TUI accesses fields by name via `DictReader`/`DictWriter`, not by index, so column position is irrelevant.

**Migration approach**: `_validate_csv_schema` currently raises on schema mismatch. We relax validation: if the header matches the *old* 11-column schema, the store upgrades it silently (adds `ID` column populated by empty string) in memory. On the next `save_tasks` call, IDs are assigned and the new header is written. This makes migration lazy and non-destructive — the file is only rewritten when a mutation happens.

### ID-based CRUD: new functions alongside old index-based ones
Add `update_task_by_id` and `delete_task_by_id` alongside the existing `update_task` and `delete_task`. The TUI continues to use the index-based forms internally (it works with a pre-loaded list and an index). CLI commands use the ID-based forms. This avoids a TUI refactor in the same PR.

**Alternative considered**: Replace index-based functions entirely — cleaner, but the TUI would need simultaneous refactoring, increasing PR scope and risk.

### File locking: `filelock` library
`filelock` is cross-platform (works on macOS, Linux, Windows), well-maintained, and requires no OS-specific code paths. A 10-second timeout surfaces the lock file path in the error message so users can diagnose a stale lock.

**Alternative considered**: stdlib `fcntl.flock` — POSIX-only (breaks on Windows); overkill for a personal tool but ruled out for portability.

### `--json` output: task as flat dict
All JSON-emitting commands use a single serializer (`task_to_dict(task) -> dict`) that maps the Task dataclass to a flat JSON object with snake_case keys matching the internal field names. This is the format agents consume from `knbn add`, `knbn edit`, and `knbn list`.

### `knbn config` is read-only, no flags
The command always dumps the full board config. Subkeys (e.g. `knbn config statuses`) would be useful but scope creep; agents can `jq` the output.

### Data-directory README: copy-once, never overwrite
The template lives at `src/knbn/defaults/README.md` and is read via `importlib.resources` (same pattern as `defaults/settings.json`). `ensure_data_dir` writes it only when `README.md` is absent. This mirrors the CLAUDE.md convention: knbn provides the starting point, the user owns the file from that point on.

The template is written in plain Markdown so any agent or human can read it with a text editor or a `cat`. It is intentionally verbose rather than terse — the goal is that an agent with no prior knowledge of knbn can read the file and issue correct CLI commands without needing external documentation.

## Risks / Trade-offs

**CSV migration is lazy (write-triggered)**
→ Mitigation: On `load_tasks`, detect old schema and transparently upgrade the in-memory list. The file is only rewritten on the next mutation. Until then the on-disk file is unchanged. This means an old `knbn` reading the same directory after a new `knbn` has partially migrated will see the new schema — fine, since old `knbn` would reject it with a `ValueError` anyway.

**Index-based TUI functions remain**
→ Mitigation: Keep `update_task` and `delete_task` as internal helpers; do not remove them. Mark them private-ish (no docstring, not exported). Plan to remove in a future version once the TUI is migrated to ID-based lookups.

**`filelock` is a new runtime dependency**
→ Mitigation: It is a tiny, zero-dependency pure-Python package. Add to `[project.dependencies]` in `pyproject.toml`.

**`--json` output mixes with Click's stderr error messages**
→ Mitigation: All Click error output goes to stderr by default; JSON goes to stdout. Scripts that capture stdout are safe.

## Migration Plan

1. Add `filelock` to `pyproject.toml` dependencies.
2. Update `Task` dataclass to add `id` field (empty default).
3. Update `_CSV_FIELDNAMES` to add `ID` as first element.
4. Update `_validate_csv_schema`: detect old 11-column schema → load rows with empty IDs; detect new 12-column schema → normal path; anything else → `ValueError`.
5. Update `_task_to_row` / `_row_to_task` for the `ID` column.
6. Add `generate_id()`, `_ensure_ids()` helpers.
7. Wrap `save_tasks` in the file lock; call `_ensure_ids()` before writing.
8. Add `update_task_by_id`, `delete_task_by_id`, `find_task_by_id`, `TaskNotFoundError`.
9. Update `ensure_data_dir` to write `db_version` to `settings.json`.
10. Add `knbn list`, `knbn edit`, `knbn delete`, `knbn config` to `cli.py`.
11. Add `--json` to `knbn add`.
12. Update `tests/fixtures/tasks.csv` to add `ID` column with pre-generated IDs.
13. Write bundled `src/knbn/defaults/README.md` template covering all task fields and CLI commands.
14. Update `ensure_data_dir` to copy the template to the data directory (skip if already present).
15. Update all affected tests; add new tests for the new CLI commands.

Rollback: The CSV migration is backward-compatible. Old schema on disk is untouched until a mutation occurs. If rolling back to a pre-ID version, the old code will reject the new-schema file with a `ValueError` on `_validate_csv_schema` — users would need to remove the `ID` column manually. This is acceptable for a personal CLI tool.
