## ADDED Requirements

### Requirement: Board config schema in settings.json
The system SHALL store board configuration under a top-level `board` key in `settings.json`. The `board` object SHALL contain: `active_statuses` (list of 2–5 non-empty strings), `default_active_status` (one value from `active_statuses`), `terminal_statuses` (list of 1–3 non-empty strings), `default_terminal_status` (one value from `terminal_statuses`), `priorities` (list of 1–5 non-empty strings ordered highest-to-lowest), `categories` (list of 1–10 objects each with `name` string and `color` hex string), and `free_text_fields` (list of 0–3 strings, empty string means slot unused).

#### Scenario: Valid board config loads successfully
- **WHEN** `settings.json` contains a `board` key with all required fields within allowed counts
- **THEN** `load_board_config()` returns a `BoardConfig` dataclass with all values populated

#### Scenario: Missing board key triggers defaults
- **WHEN** `settings.json` exists but has no `board` key
- **THEN** `load_board_config()` returns the built-in default `BoardConfig` (active: `['Todo', 'Now', 'Feedback']`, default active: `'Now'`, terminal: `['Done', 'Delegated', 'Stopped']`, default terminal: `'Done'`, priorities: `['High', 'Medium', 'Low']`, categories matching the seven legacy defaults, free_text_fields: `['Feedback From', 'Delegated To', '']`)

#### Scenario: settings.json absent triggers defaults
- **WHEN** `settings.json` does not exist
- **THEN** `load_board_config()` returns the built-in default `BoardConfig`

### Requirement: Board config validation
The system SHALL validate the `board` block on load and raise `BoardConfigError` with a descriptive message if any of the following violations are found: fewer than 2 or more than 5 active statuses, fewer than 1 or more than 3 terminal statuses, `default_active_status` not in `active_statuses`, `default_terminal_status` not in `terminal_statuses`, fewer than 1 or more than 5 priorities, fewer than 1 or more than 10 categories, more than 3 entries in `free_text_fields`.

#### Scenario: Too few active statuses rejected
- **WHEN** `board.active_statuses` contains only one entry
- **THEN** `load_board_config()` raises `BoardConfigError` naming the constraint

#### Scenario: Default status not in list rejected
- **WHEN** `board.default_active_status` is a value not present in `board.active_statuses`
- **THEN** `load_board_config()` raises `BoardConfigError` naming the mismatch

#### Scenario: Too many categories rejected
- **WHEN** `board.categories` contains 11 entries
- **THEN** `load_board_config()` raises `BoardConfigError`

### Requirement: BoardConfig dataclass
The system SHALL expose a `BoardConfig` dataclass (importable from `knbn.config`) with typed fields: `active_statuses: list[str]`, `default_active_status: str`, `terminal_statuses: list[str]`, `default_terminal_status: str`, `priorities: list[str]`, `categories: list[CategoryConfig]`, `free_text_fields: list[str]`. `CategoryConfig` SHALL be a dataclass with `name: str` and `color: str`. Helper methods SHALL include `category_color(name: str) -> str` (returns configured hex or `'#888888'` fallback), `active_free_text_fields() -> list[tuple[int, str]]` (returns `(index, label)` pairs for non-empty entries only), and `all_statuses() -> list[str]` (active + terminal concatenated).

#### Scenario: category_color returns configured value
- **WHEN** `board_config.category_color('Engineering')` is called and Engineering has color `'#4dbfbf'` in config
- **THEN** `'#4dbfbf'` is returned

#### Scenario: category_color falls back for unknown category
- **WHEN** `board_config.category_color('UnknownTag')` is called
- **THEN** `'#888888'` is returned

#### Scenario: active_free_text_fields skips empty slots
- **WHEN** `free_text_fields` is `['Feedback From', '', 'Notes']`
- **THEN** `active_free_text_fields()` returns `[(0, 'Feedback From'), (2, 'Notes')]`

### Requirement: Auto-assigned category colors
The system SHALL assign a color to each category from a fixed 10-color palette when generating default or wizard-created board config. Colors SHALL be assigned in palette order cycling as needed. The palette SHALL include (in order): `#e879a0`, `#f4a7b9`, `#7ec8e3`, `#5b9bd5`, `#4dbfbf`, `#f5a623`, `#cccccc`, `#a78bfa`, `#34d399`, `#fbbf24`. A manually specified color in `settings.json` SHALL always take precedence over palette assignment.

### Requirement: Category color format
Every category `color` value SHALL be a 6-digit lowercase hex string prefixed with `#` (e.g. `#4dbfbf`). `load_board_config()` SHALL reject any color value that does not match the pattern `#[0-9a-f]{6}` with a `BoardConfigError`.

#### Scenario: Valid 6-digit hex accepted
- **WHEN** a category has `color` value `"#4dbfbf"`
- **THEN** `load_board_config()` loads successfully

#### Scenario: Short hex rejected
- **WHEN** a category has `color` value `"#fff"`
- **THEN** `load_board_config()` raises `BoardConfigError` naming the invalid color

#### Scenario: Uppercase hex rejected
- **WHEN** a category has `color` value `"#4DBFBF"`
- **THEN** `load_board_config()` raises `BoardConfigError` naming the invalid color

#### Scenario: Missing hash rejected
- **WHEN** a category has `color` value `"4dbfbf"`
- **THEN** `load_board_config()` raises `BoardConfigError` naming the invalid color

#### Scenario: First category gets first palette color
- **WHEN** a board config is generated with one category `'Work'` and no explicit color
- **THEN** `Work` is assigned color `'#e879a0'`

#### Scenario: Eleventh category cycles palette
- **WHEN** ten categories are already assigned and an eleventh is added via settings.json
- **THEN** the eleventh category is assigned color `'#e879a0'` (palette index 0)

