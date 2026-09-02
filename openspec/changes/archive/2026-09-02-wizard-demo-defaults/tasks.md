## 1. Defaults package data file

- [x] 1.1 Create `src/knbn/defaults/` directory with an empty `__init__.py` and a `settings.json` containing the full board config from `demo/settings.json`; verify `uv build` includes the JSON file in the wheel (check with `unzip -l dist/*.whl | grep defaults`)
- [x] 1.2 Add a test `tests/test_defaults_sync.py` that loads both `demo/settings.json` and the packaged `knbn/defaults/settings.json` and asserts their `board` blocks are identical; verify the test passes with `uv run pytest tests/test_defaults_sync.py`

## 2. `load_default_board_config()` in config.py

- [x] 2.1 Add `load_default_board_config() -> dict` to `knbn/config.py` using `importlib.resources.files("knbn").joinpath("defaults/settings.json")` to read and parse the file; raise `RuntimeError` with a descriptive message on missing file or invalid JSON; verify with a unit test in `tests/test_config.py`
- [x] 2.2 Replace the hardcoded `BOARD_CONFIG_DEFAULTS` dict in `config.py` with a call to `load_default_board_config()` (assigned at module level so existing callers are unaffected); update `build_default_board_config()` and `SETTINGS_DEFAULTS` to derive from the loader; verify `uv run pytest tests/test_config.py` and `uv run mypy src/` both pass

## 3. Wizard quick-start prompt

- [x] 3.1 Add a quick-start prompt as the first step in `run_setup_wizard()` in `src/knbn/setup.py`: print "Use standard settings? [Y/n]", call `load_default_board_config()` on acceptance, write the result as the `board` block via `save_settings()`, print a confirmation line, and return early; verify with a unit test that patches `click.prompt` to return `""` (accept) and asserts `save_settings` is called with the default config dict
- [x] 3.2 Add a unit test covering the decline path (`n` input) that asserts the wizard proceeds to the active-status collection step; verify with `uv run pytest tests/test_setup.py`

## 4. Full build verification

- [x] 4.1 Run `make build` and confirm all checks pass (tests, mypy, lint, format, uv build)
