## 1. Update packaged defaults

- [x] 1.1 In `src/knbn/defaults/settings.json`, replace the `board.categories` list with three entries — `Personal`, `Work`, `Other` — assigning colors from `CATEGORY_COLOR_PALETTE` (`src/knbn/config.py`) in order (`#e879a0`, `#f4a7b9`, `#7ec8e3`). Verify by loading the file as JSON and confirming exactly 3 category objects with those names and colors.
- [x] 1.2 Confirm `demo/settings.json` and `demo/tasks.csv` are left untouched (categories stay `People`, `Strategy`, `Product`, `Engineering`, `Other`). Verify with `git diff --stat demo/` showing no changes.

## 2. Retire the defaults/demo sync invariant

- [x] 2.1 Delete `tests/test_defaults_sync.py` — the packaged defaults and demo fixture are now intentionally allowed to diverge. Verify by confirming the file no longer exists and `uv run pytest tests -k defaults_sync` collects zero tests.

## 3. Update tests that assume the old defaults

- [x] 3.1 In `tests/test_board_config.py::test_build_default_board_config_returns_legacy_defaults`, update the category assertions to expect 3 categories named `Personal`, `Work`, `Other` (update the assertion `len(cfg.categories) == 5` and add/adjust name checks). Verify with `uv run pytest tests/test_board_config.py -k legacy_defaults`.
- [x] 3.2 Search `tests/` for any other assertion that hardcodes the old default category names or count (`People`, `Strategy`, `Engineering`, or `== 5`/`== 7` category counts tied to `build_default_board_config()`/`load_default_board_config()`) and update them. Verify with `grep -rn "People\|Strategy\|Engineering" tests/` returning only demo-data-driven tests, if any.

## 4. Sync the spec and validate

- [x] 4.1 Confirm `openspec/specs/board-config/spec.md` will pick up the updated "Missing board key triggers defaults" scenario and the new "Built-in defaults are independent of the demo dataset" scenario on archive (no action beyond what's already in this change's delta spec). Verify with `openspec validate update-default-categories --strict`.

## 5. Full verification

- [x] 5.1 Run `make build` (tests + mypy + lint + format + uv build) and confirm it passes clean.
