## 1. Settings Helpers

- [x] 1.1 Add `SETTINGS_DEFAULTS: dict[str, str] = {'theme': 'dark'}` and `_SETTINGS_FILENAME = 'settings.json'` constants to `src/knbn/config.py`
- [x] 1.2 Implement `load_settings(data_dir: Path) -> dict[str, str]` in `config.py`: reads `settings.json`, merges with `SETTINGS_DEFAULTS`, returns merged dict; returns defaults if file absent or malformed
- [x] 1.3 Implement `save_settings(data_dir: Path, settings: dict[str, str]) -> None` in `config.py`: atomic write via `.settings.json.tmp` → rename
- [x] 1.4 Implement `get_setting(data_dir: Path, key: str, default: str = '') -> str` convenience wrapper in `config.py`

## 2. Data Directory Init

- [x] 2.1 Update `ensure_data_dir` in `src/knbn/model/store.py` to create `settings.json` with defaults if it does not exist (call `save_settings` only when the file is absent)

## 3. TUI Theme Integration

- [x] 3.1 In the `board` command in `src/knbn/cli.py`, read `theme` via `get_setting` and pass it to `KnbnApp(data_dir=data_dir, theme=theme)`
- [x] 3.2 Update `KnbnApp.__init__` in `src/knbn/app.py` to accept and forward the `theme` parameter to `super().__init__(theme=theme)`

## 4. Tests

- [x] 4.1 Add `tests/test_settings.py`: test `load_settings` returns defaults for missing file, test round-trip (save → load), test atomic write uses `.tmp` file, test `get_setting` with present and absent keys
- [x] 4.2 Update `tests/test_store.py`: verify `ensure_data_dir` creates `settings.json` alongside `tasks.csv` and `notes/`

## 5. Verification

- [x] 5.1 Run `uv run pytest -q` and confirm all tests pass at ≥95% coverage
- [x] 5.2 Run `uv run ruff check src/ tests/` and `uv run mypy src/` with no errors
- [x] 5.3 Smoke-test: set `{"theme": "light"}` in `~/.knbn/settings.json`, run `knbn board`, confirm light theme loads
