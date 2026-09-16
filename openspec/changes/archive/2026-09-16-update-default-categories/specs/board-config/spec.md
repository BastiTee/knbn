## MODIFIED Requirements

### Requirement: Board config schema in settings.json
The system SHALL store board configuration under a top-level `board` key in `settings.json`. The `board` object SHALL contain: `active_statuses` (list of 2–5 non-empty strings), `default_active_status` (one value from `active_statuses`), `terminal_statuses` (list of 1–3 non-empty strings), `default_terminal_status` (one value from `terminal_statuses`), `priorities` (list of 1–5 non-empty strings ordered highest-to-lowest), `categories` (list of 1–10 objects each with `name` string and `color` hex string), and `free_text_fields` (list of 0–3 strings, empty string means slot unused).

#### Scenario: Valid board config loads successfully
- **WHEN** `settings.json` contains a `board` key with all required fields within allowed counts
- **THEN** `load_board_config()` returns a `BoardConfig` dataclass with all values populated

#### Scenario: Missing board key triggers defaults
- **WHEN** `settings.json` exists but has no `board` key
- **THEN** `load_board_config()` returns the built-in default `BoardConfig` (active: `['Todo', 'Now', 'Feedback']`, default active: `'Now'`, terminal: `['Done', 'Delegated', 'Stopped']`, default terminal: `'Done'`, priorities: `['High', 'Medium', 'Low']`, categories: `Personal`, `Work`, `Other`, free_text_fields: `['Feedback From', 'Delegated To', '']`)

#### Scenario: settings.json absent triggers defaults
- **WHEN** `settings.json` does not exist
- **THEN** `load_board_config()` returns the built-in default `BoardConfig`

#### Scenario: Built-in defaults are independent of the demo dataset
- **WHEN** the built-in default categories (`Personal`, `Work`, `Other`) are compared against the categories used in the bundled demo dataset (`demo/settings.json`, `demo/tasks.csv`)
- **THEN** the two category sets are allowed to differ, and no test or build step SHALL require them to match
