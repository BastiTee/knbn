## MODIFIED Requirements

### Requirement: Settings structure
`settings.json` SHALL have exactly two top-level keys: `app` (a nested dict holding application-level settings) and `board` (a nested dict holding board configuration). There SHALL be no flat top-level settings keys. The `app` block SHALL contain `theme` and `deadline_warning_hours`. The `board` block is defined in the board-config spec. Both blocks default gracefully when absent.

#### Scenario: settings.json structure
- **WHEN** `settings.json` is written by the system
- **THEN** it contains only the `app` and `board` top-level keys with nested dicts

### Requirement: Settings load and save
The system SHALL provide functions to load all settings from `settings.json` as a `dict[str, Any]`, get a setting from the `app` block by key (returning a default if absent), and save the full settings dict back to `settings.json` atomically. `load_settings` SHALL merge each top-level block shallowly: file values win over defaults for every key present in the file.

#### Scenario: Load returns defaults for missing file
- **WHEN** `settings.json` does not exist
- **THEN** `load_settings` returns a dict with default `app` and `board` blocks

#### Scenario: Get app setting
- **WHEN** `get_app_setting('theme')` is called and `settings.json` contains `{"app": {"theme": "nord"}}`
- **THEN** `'nord'` is returned

#### Scenario: Get app setting with missing key returns default
- **WHEN** `get_app_setting('theme', 'textual-dark')` is called and the `app` block has no `theme` key
- **THEN** `'textual-dark'` is returned

#### Scenario: Save is atomic
- **WHEN** `save_settings` is called
- **THEN** the write goes to a `.settings.json.tmp` file first, then renamed to `settings.json`

#### Scenario: Both blocks preserved on save
- **WHEN** `save_settings` is called with a dict containing both `app` and `board` blocks
- **THEN** the resulting `settings.json` contains both nested blocks intact

## ADDED Requirements

### Requirement: Board config defaults
The system SHALL define a `BOARD_CONFIG_DEFAULTS` constant representing the legacy-compatible default board configuration: `active_statuses: ['Todo', 'Now', 'Feedback']`, `default_active_status: 'Now'`, `terminal_statuses: ['Done', 'Delegated', 'Stopped']`, `default_terminal_status: 'Done'`, `priorities: ['High', 'Medium', 'Low']`, seven categories matching the legacy defaults with their existing colors, and `free_text_fields: ['Feedback From', 'Delegated To', '']`.

#### Scenario: Default board config matches legacy behavior
- **WHEN** `load_board_config()` is called with no `settings.json`
- **THEN** the returned `BoardConfig` has `active_statuses == ['Todo', 'Now', 'Feedback']`, `default_terminal_status == 'Done'`, and `priorities == ['High', 'Medium', 'Low']`

### Requirement: Settings file initialization
The system SHALL create a `settings.json` file in the data directory when initializing. If the file does not exist, it SHALL be created with default `app` and `board` blocks. `ensure_data_dir` SHALL be responsible for creating it alongside `tasks.csv` and `notes/`.

#### Scenario: Settings file created on init
- **WHEN** `knbn init` is called on a fresh data directory
- **THEN** `settings.json` is created alongside `tasks.csv` and `notes/`

#### Scenario: Settings file preserved if already exists
- **WHEN** `knbn init` is called and `settings.json` already exists with custom values
- **THEN** the existing `settings.json` is not overwritten

### Requirement: Theme setting
The system SHALL support a `theme` setting under the `app` block whose value is any Textual theme name. The default value SHALL be `textual-dark`. The TUI SHALL read `settings["app"]["theme"]` on startup and apply the corresponding Textual theme.

#### Scenario: Default theme is textual-dark
- **WHEN** no `settings.json` exists or the `app.theme` key is absent
- **THEN** the TUI launches with the `textual-dark` theme

#### Scenario: Alternative theme applied
- **WHEN** `settings.json` contains `{"app": {"theme": "nord"}}`
- **THEN** the TUI launches with the `nord` theme

### Requirement: Deadline warning hours setting
The system SHALL support a `deadline_warning_hours` setting under the `app` block controlling how many hours before a task's due date the Kanban card warning highlight is shown. The default SHALL be `24`. Invalid values SHALL silently fall back to `24`.

#### Scenario: Default deadline_warning_hours is 24
- **WHEN** no `settings.json` exists or the `app.deadline_warning_hours` key is absent
- **THEN** the deadline warning window is 24 hours

#### Scenario: Custom deadline_warning_hours applied
- **WHEN** `settings.json` contains `{"app": {"deadline_warning_hours": "48"}}`
- **THEN** the deadline warning highlight appears on cards with a due date within 48 hours
