## Context

`config.py` already contains `BOARD_CONFIG_DEFAULTS` — a hardcoded Python dict with the same values as `demo/settings.json`. The wizard currently has no quick-start path; every new install must go through five interactive steps. The risk is that `BOARD_CONFIG_DEFAULTS` and `demo/settings.json` drift apart silently as the project evolves.

## Goals / Non-Goals

**Goals:**
- Single source of truth for the default board config (one file, no duplicated data)
- Wizard offers a "use standard settings" shortcut on first run
- Changing the defaults file automatically changes what the wizard offers, with no code edits

**Non-Goals:**
- Replacing `demo/settings.json` as a human-readable reference (it stays; it just becomes a copy)
- Changing anything about the interactive wizard steps (they remain unchanged for users who decline)
- Migrating existing installations or touching `load_board_config()` behavior

## Decisions

### Decision: Package-data file as single source of truth

Ship `src/knbn/defaults/settings.json` as package data. Remove the hardcoded `BOARD_CONFIG_DEFAULTS` dict from `config.py` and replace it with a `load_default_board_config() -> dict` function that reads the file via `importlib.resources.files("knbn").joinpath("defaults/settings.json")`.

**Why not keep the hardcoded dict?** The user's requirement is "change the config without rewriting code." A Python dict in source *is* code; a JSON file is data.

**Why `importlib.resources` over a path relative to `__file__`?** `importlib.resources` works correctly in editable installs, zip-packaged distributions, and namespace packages. Path-relative hacks break in at least one of those cases.

**Alternative considered:** Keep `demo/settings.json` as the source and read it at runtime. Rejected: `demo/` is not inside the `knbn` package and is not shipped in distributions — it is a dev-time artifact.

### Decision: `demo/settings.json` becomes a copy, not a symlink

After this change, `demo/settings.json` and `src/knbn/defaults/settings.json` contain the same board config. Keeping them as two files (rather than a symlink) is safer for cross-platform compatibility and avoids confusing users who look at the demo directory. A test asserts they are identical to catch drift.

### Decision: `BOARD_CONFIG_DEFAULTS` is replaced, not kept as alias

`build_default_board_config()` and `SETTINGS_DEFAULTS` currently reference `BOARD_CONFIG_DEFAULTS`. After this change, `build_default_board_config()` calls `load_default_board_config()` directly. `SETTINGS_DEFAULTS` is updated the same way. The public name `BOARD_CONFIG_DEFAULTS` is removed (it was not part of any public API contract; it was an internal constant).

## Risks / Trade-offs

- **File I/O at import time** → Mitigation: `load_default_board_config()` is called lazily (only from `build_default_board_config()` and the wizard), never at module import. No startup cost.
- **`defaults/settings.json` must be declared in `pyproject.toml`** → If omitted, the file is missing in installed packages and `load_default_board_config()` raises `RuntimeError`. Mitigation: a test that calls the function in the installed package verifies it.
- **`demo/settings.json` drift** → A test compares the two files and fails if they diverge.
