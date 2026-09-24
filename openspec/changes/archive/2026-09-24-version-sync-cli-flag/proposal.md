## Why

When `knbn` is upgraded to a new release, the `db_version` key in `settings.json` can remain stale because read-only commands like `knbn config` do not call `ensure_data_dir` — only modifying commands update it. Additionally, there is no way to ask `knbn` which version is installed without inspecting the package metadata manually.

## What Changes

- Add a `--version` flag to the `knbn` CLI root command that prints the installed package version and exits.
- Ensure `db_version` in `settings.json` is refreshed to the current package version on every command invocation, including read-only ones (`config`).

## Capabilities

### New Capabilities

- `cli-version-flag`: A `--version` / `-V` option on the root `knbn` command group that outputs the installed package version string (sourced from `importlib.metadata`) and exits with code 0.

### Modified Capabilities

- `db-version`: Extend the requirement that `db_version` is kept current: it must be written (or verified) on every knbn command invocation that touches the data directory, not only on store-initialisation and migration.

## Impact

- `src/knbn/cli.py`: add `@click.version_option(...)` to the `cli` group; add `ensure_data_dir` call (or equivalent) to the `config` command.
- `src/knbn/model/store.py`: no structural change needed — `_write_db_version` already handles the idempotent write.
- `demo/settings.json`: update `db_version` to match the current release (maintenance-only, no code change).
- No new dependencies; `importlib.metadata` is stdlib ≥ 3.8 and already used by `store.py`.
