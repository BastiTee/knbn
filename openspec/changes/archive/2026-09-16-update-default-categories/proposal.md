## Why

The bundled default board config (`src/knbn/defaults/settings.json`) ships five work-oriented categories (`People`, `Strategy`, `Product`, `Engineering`, `Other`) inherited from the demo dataset. These don't fit a general personal-kanban audience. New stores should default to a small, generic set — `Personal`, `Work`, `Other` — without touching the demo data's richer categories, which exist to showcase the tool's category feature across a realistic dataset.

## What Changes

- Change the `board.categories` list in `src/knbn/defaults/settings.json` (the packaged defaults new stores are built from) to three entries: `Personal`, `Work`, `Other`, with colors assigned from `CATEGORY_COLOR_PALETTE` in order.
- **BREAKING**: New stores created with default settings (via `knbn init` or the wizard's quick-start) now get 3 categories instead of 5, with different names. Existing `~/.knbn/settings.json` files are unaffected (categories are only read from the bundled defaults when no user settings exist).
- Leave `demo/settings.json` and `demo/tasks.csv` unchanged — the demo dataset keeps `People`, `Strategy`, `Product`, `Engineering`, `Other` so the shipped demo continues to look like a populated, realistic board.
- Retire the `tests/test_defaults_sync.py` assertion that `src/knbn/defaults/settings.json` and `demo/settings.json` must be byte-for-byte identical. That invariant is now intentionally false: the packaged defaults and the demo fixture are allowed to diverge going forward.
- Update the one test that hardcodes the current default category count (`tests/test_board_config.py::test_build_default_board_config_returns_legacy_defaults`, `len(cfg.categories) == 5`) to expect 3.

## Capabilities

### Modified Capabilities
- `board-config`: the built-in default `BoardConfig` categories change from the five legacy demo-derived categories to `Personal`, `Work`, `Other`; the requirement text describing "categories matching the seven legacy defaults" is corrected to describe the new default set and no longer implies parity with the demo dataset.

## Impact

- `src/knbn/defaults/settings.json` — categories list changed.
- `demo/settings.json`, `demo/tasks.csv` — unchanged (explicitly out of scope).
- `tests/test_defaults_sync.py` — removed (the sync invariant it enforced no longer holds).
- `tests/test_board_config.py` — one assertion updated to the new category count.
- `openspec/specs/board-config/spec.md` — scenario text describing the built-in defaults updated.
- New installs (`knbn init`, wizard quick-start) get the new default categories; existing installs are unaffected since they already have a `settings.json` with their own `categories`.
