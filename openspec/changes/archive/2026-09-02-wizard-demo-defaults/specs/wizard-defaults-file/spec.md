## Purpose

Defines a bundled defaults file shipped inside the `knbn` package that provides a ready-to-use board configuration preset, allowing the setup wizard and any other caller to load standard settings without hardcoding values in application logic.

## ADDED Requirements

### Requirement: Defaults file location
The `knbn` package SHALL ship a file at `knbn/defaults/settings.json` containing a complete, valid board configuration under the `board` key. The file SHALL be declared as package data so it is included in installed distributions and editable installs alike.

#### Scenario: Defaults file present after install
- **WHEN** `knbn` is installed via `pip` or `uv`
- **THEN** `importlib.resources.files("knbn").joinpath("defaults/settings.json")` resolves to a readable file

### Requirement: Defaults file content
The `board` block in `knbn/defaults/settings.json` SHALL be kept in sync with `demo/settings.json`. The file SHALL be valid JSON. Its `board` block SHALL satisfy all constraints defined in the `board-config` spec (valid statuses, priorities, categories, free-text fields).

#### Scenario: Defaults file is parseable
- **WHEN** the defaults file is read at runtime
- **THEN** `json.loads()` succeeds without error and the result contains a `board` key

### Requirement: Defaults loader function
A public function `load_default_board_config() -> dict` SHALL be exposed from `knbn.config`. It SHALL read `knbn/defaults/settings.json` via `importlib.resources`, parse its `board` block, and return it as a plain `dict`. It SHALL raise `RuntimeError` with a descriptive message if the file is missing or not valid JSON.

#### Scenario: Loader returns board config dict
- **WHEN** `load_default_board_config()` is called
- **THEN** it returns a dict with keys `active_statuses`, `terminal_statuses`, `priorities`, `categories`, and `free_text_fields`

#### Scenario: Loader raises on corrupt file
- **WHEN** the defaults file contains invalid JSON
- **THEN** `load_default_board_config()` raises `RuntimeError`
