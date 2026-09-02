## Why

New users hitting the setup wizard for the first time must answer five configuration steps cold — with no guidance on sensible values for statuses, priorities, categories, and free-text fields. The project already ships a demo `settings.json` with a well-considered default configuration; there is no reason to make users reinvent it.

## What Changes

- Add a **quick-start prompt** as the first step of the board setup wizard: "Use standard settings? [Y/n]"
- If the user accepts, the wizard reads the board config block from a **bundled defaults file** (shipped with the package) and writes it directly to `settings.json`, skipping all individual configuration steps
- The defaults file is **not hardcoded** in wizard logic — it is loaded at runtime so updating the file changes what the wizard offers without any code changes
- If the user declines, the wizard continues with the existing interactive steps unchanged
- The bundled defaults file mirrors the current `demo/settings.json` board config and lives at a discoverable path inside the package (e.g., `knbn/defaults/settings.json`)

## Capabilities

### New Capabilities

- `wizard-defaults-file`: A bundled `defaults/settings.json` shipped inside the `knbn` package that serves as the authoritative source for the quick-start preset. Defines where the file lives and how it is located at runtime.

### Modified Capabilities

- `board-setup-wizard`: New first step ("Use standard settings?") that short-circuits the wizard by loading the defaults file instead of prompting each configuration step individually.

## Impact

- `src/knbn/` — new `defaults/` directory with `settings.json` (package data, included via `pyproject.toml`)
- `src/knbn/cli.py` — wizard gains a quick-start branch that reads `defaults/settings.json` via `importlib.resources`
- `demo/settings.json` — remains the human-facing reference; its board block is kept in sync with `defaults/settings.json`
- `pyproject.toml` — must include `defaults/settings.json` as package data
