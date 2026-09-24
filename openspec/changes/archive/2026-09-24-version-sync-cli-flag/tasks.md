## 1. CLI --version flag

- [x] 1.1 Add `@click.version_option(package_name="knbn", prog_name="knbn")` decorator to the `cli` group in `src/knbn/cli.py` and verify `uv run knbn --version` and `uv run knbn -V` each print `knbn, version X.Y.Z` and exit 0
- [x] 1.2 Add a unit test in `tests/test_cli.py` that invokes the root `cli` with `["--version"]` via Click's `CliRunner` and asserts the output contains the package version string from `importlib.metadata.version("knbn")`

## 2. db_version refresh on read-only commands

- [x] 2.1 Add `ensure_data_dir(data_dir)` call at the start of the `config` command in `src/knbn/cli.py` (before `load_settings`) and verify `uv run knbn config` after a simulated version mismatch updates `db_version` in `settings.json`
- [x] 2.2 Add or extend a unit test in `tests/test_cli.py` covering the `config` command: write a `settings.json` with an old `db_version`, run `knbn config`, and assert the returned JSON contains the current installed version in `db_version`

## 3. Fixture maintenance

- [x] 3.1 Update `demo/settings.json` to set `"db_version"` to the current release version (`0.3.0`) and verify the file is valid JSON (`python3 -m json.tool demo/settings.json`)
