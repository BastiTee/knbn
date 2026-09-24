## Context

The `knbn` CLI uses Click for command dispatch. The root `cli` group currently has no `--version` option. Version information is available at runtime via `importlib.metadata.version("knbn")`, which is already used in `store.py`'s `_write_db_version`.

`db_version` is written idempotently by `_write_db_version` (in `store.py`): it reads settings, compares to the current package version, and writes only when they differ. `ensure_data_dir` calls `_write_db_version` unconditionally, so any command that calls `ensure_data_dir` already refreshes `db_version`. The gap is the `config` command, which reads settings and displays `db_version` but does not call `ensure_data_dir`, meaning it can show a stale value immediately after an upgrade.

See `proposal.md` for motivation.

## Goals / Non-Goals

**Goals:**
- Add `--version` / `-V` to the `knbn` root command using Click's built-in `version_option`.
- Guarantee `db_version` in `settings.json` equals the installed version after any command that uses the data directory.

**Non-Goals:**
- Version history, changelog output, or upgrade notifications.
- Checking for newer releases on PyPI.
- Changing the `db_version` semantics (it remains the installed package version, not a separate schema version).

## Decisions

### Use Click's built-in `version_option`
Click provides `@click.version_option(package_name="knbn")` which calls `importlib.metadata.version` internally and handles `--version` / `-V`, `is_eager=True` (runs before subcommand dispatch), and `expose_value=False`. This avoids duplicating the version-flag logic by hand.

Alternative considered: `@click.option("--version", ...)` with a custom callback. Rejected because `version_option` already does exactly this and is idiomatic Click.

### Fix `config` by calling `ensure_data_dir`
The `config` command will call `ensure_data_dir(data_dir)` before reading settings, consistent with every other command. This is the minimal, already-tested path.

Alternative considered: call `_write_db_version` directly in `config`. Rejected because it would import a private store function into `cli.py` and duplicate the pattern already handled by `ensure_data_dir`.

### Update `demo/settings.json` manually as a maintenance step
`demo/settings.json` is a static fixture. Its `db_version` field will be bumped to the current release version as a one-off task; no automated mechanism is needed since the file is not a live data directory.

## Risks / Trade-offs

- `ensure_data_dir` creates the data directory and CSV if missing. Adding it to `config` means `knbn config` can now create `~/.knbn` as a side-effect on a fresh machine. This is acceptable — `config` is the natural first command a user runs to inspect their setup.

## Migration Plan

No migration required. Changes are backward-compatible:
- `--version` is a new flag with no interaction with existing commands.
- `ensure_data_dir` in `config` is additive; existing stores are unaffected.
- `demo/settings.json` update is a checked-in file change with no user-facing impact.
