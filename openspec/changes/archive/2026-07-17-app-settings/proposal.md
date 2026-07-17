## Why

Currently `knbn` stores no user preferences — settings like the UI theme have nowhere to live. Rather than adding ad-hoc env vars or hard-coding values, introducing a general `settings.json` in the data directory gives all future user preferences a stable, discoverable home.

## What Changes

- **New `settings.json`** in the data directory (`~/.knbn/settings.json`) holding user preferences as a JSON object
- **New `theme` setting**: one of `dark` (default) or `light`; read at TUI startup and applied to the Textual app
- `ensure_data_dir` updated to create a default `settings.json` if absent
- `config.py` extended with `load_settings` / `save_settings` / `get_setting` / `set_setting` helpers

## Capabilities

### New Capabilities

- `app-settings`: A general settings file in the data directory storing user preferences, with TUI integration for the theme setting

### Modified Capabilities

## Impact

- `src/knbn/config.py` — new settings load/save helpers
- `src/knbn/app.py` — read `theme` setting on startup and pass to Textual
- `src/knbn/model/store.py` — `ensure_data_dir` creates default `settings.json`
- `tests/` — new tests for settings load/save
- No new dependencies
