## Purpose

Defines the requirements for persisted application settings in `knbn`. Settings are stored as JSON in the data directory and control runtime behaviour such as the TUI theme.

## Requirements

### Requirement: Settings file initialization
The system SHALL create a `settings.json` file in the data directory when initializing. If the file does not exist, it SHALL be created with all default values. `ensure_data_dir` SHALL be responsible for creating it alongside `tasks.csv` and `notes/`.

#### Scenario: Settings file created on init
- **WHEN** `knbn init` is called on a fresh data directory
- **THEN** `settings.json` is created alongside `tasks.csv` and `notes/`

#### Scenario: Settings file preserved if already exists
- **WHEN** `knbn init` is called and `settings.json` already exists with custom values
- **THEN** the existing `settings.json` is not overwritten

### Requirement: Theme setting
The system SHALL support a `theme` setting whose value is any theme name available in Textual (e.g. `textual-dark`, `textual-light`, `dracula`, `nord`). The default value SHALL be `textual-dark`. The TUI SHALL read the `theme` setting on startup and apply the corresponding Textual theme.

#### Scenario: Default theme is textual-dark
- **WHEN** no `settings.json` exists or the `theme` key is absent
- **THEN** the TUI launches with the `textual-dark` theme

#### Scenario: Alternative theme applied
- **WHEN** `settings.json` contains `{"theme": "nord"}`
- **THEN** the TUI launches with the `nord` theme

### Requirement: Settings load and save
The system SHALL provide functions to load all settings from `settings.json` as a dict, get a single setting by key (returning a default if absent), and save the full settings dict back to `settings.json` atomically.

#### Scenario: Load returns defaults for missing file
- **WHEN** `settings.json` does not exist
- **THEN** `load_settings` returns a dict with all default values

#### Scenario: Get single setting
- **WHEN** `get_setting` is called with a key present in `settings.json`
- **THEN** the stored value is returned

#### Scenario: Get setting with missing key returns default
- **WHEN** `get_setting` is called with a key not in `settings.json`
- **THEN** the provided default value is returned

#### Scenario: Save is atomic
- **WHEN** `save_settings` is called
- **THEN** the write goes to a `.settings.json.tmp` file first, then renamed to `settings.json`

### Requirement: Deadline warning hours setting
The system SHALL support a `deadline_warning_hours` setting whose value is a positive integer (stored as a string). It controls how many hours before a task's due date the Kanban card warning highlight is shown. The default value SHALL be `24`. If the stored value is not a valid positive integer, the system SHALL silently fall back to `24`.

#### Scenario: Default deadline_warning_hours is 24
- **WHEN** no `settings.json` exists or the `deadline_warning_hours` key is absent
- **THEN** the deadline warning window is 24 hours

#### Scenario: Custom deadline_warning_hours applied
- **WHEN** `settings.json` contains `{"deadline_warning_hours": "48"}`
- **THEN** the deadline warning highlight appears on cards with a due date within 48 hours

#### Scenario: Invalid value falls back to default
- **WHEN** `settings.json` contains `{"deadline_warning_hours": "bad"}`
- **THEN** the deadline warning window falls back to 24 hours
