## Context

`knbn` currently has no persistent user preferences. The Textual `App` class accepts a `theme` parameter at construction, but there is no mechanism to read user preferences from disk. All configuration today is via environment variables (`KNBN_DATA_DIR`, `$EDITOR`), which are not suitable for user-facing preferences like theme.

The data directory (`~/.knbn/`) already exists as the natural home for user data. Adding `settings.json` there keeps preferences co-located with tasks, version-controllable if the user symlinks their data dir, and inspectable with any text editor.

## Goals / Non-Goals

**Goals:**
- A single `settings.json` in the data directory for all future user preferences
- `theme` as the first setting (values: `dark` / `light`, default `dark`)
- TUI reads `theme` at startup

**Non-Goals:**
- A CLI command for reading/writing settings (edit `settings.json` directly)
- A rich configuration UI inside the TUI
- Per-project or per-workspace settings (single file only)
- Validation beyond known allowed values for `theme`
- Live reload of settings while the TUI is running

## Decisions

### D1: JSON over TOML or INI
**Decision**: Use JSON for `settings.json`.
**Rationale**: The stdlib `json` module requires no new dependency. The file is small and machine-written; human-readability of TOML is not needed here. Consistent with the existing CSV-only, zero-extra-dependency posture.
**Alternatives considered**: TOML (needs `tomllib`/`tomli`), INI (`configparser` — no type awareness).

### D2: Settings helpers in `config.py`, not a new module
**Decision**: Add `load_settings`, `save_settings`, `get_setting` to the existing `config.py`.
**Rationale**: `config.py` already owns data-directory resolution. Settings access is a natural extension. A separate `settings.py` module would add indirection for a small amount of code.

### D3: Atomic write via `.tmp` rename
**Decision**: Write `settings.json` atomically via `.settings.json.tmp` → rename, matching the existing `save_tasks` pattern.
**Rationale**: Consistency with the store layer; prevents corruption on crash.

### D4: Theme applied via `App(theme=...)` constructor parameter
**Decision**: Read the theme from settings in `cli.py` (in the `board` command) and pass it to `KnbnApp(theme=...)`.
**Rationale**: Textual 8 accepts `theme` as a constructor parameter on `App`. Reading it at construction time is simpler than applying it after mount.

## Risks / Trade-offs

- **Settings file schema drift** → Mitigation: `load_settings` always merges against a `DEFAULTS` dict, so missing keys always return sensible values regardless of file age.
- **No CLI to edit settings** → The file is plain JSON at a known path; users edit it directly. Document the path and schema in the README.
