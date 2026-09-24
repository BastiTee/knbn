## Purpose

Read-only CLI command that emits the resolved board configuration as JSON, giving agents and scripts a stable, machine-parseable way to discover valid statuses, priorities, categories, and free-text field labels.

## ADDED Requirements

### Requirement: knbn config command
The system SHALL provide a `knbn config` subcommand that prints the fully resolved `BoardConfig` to stdout as a JSON object. The output SHALL always be valid JSON and SHALL include the following top-level keys:

- `active_statuses` — ordered array of active status strings
- `default_active_status` — string
- `terminal_statuses` — ordered array of terminal status strings
- `default_terminal_status` — string
- `priorities` — ordered array of priority strings
- `categories` — array of objects with `name` (string) and `color` (hex string)
- `free_text_fields` — array of 3 label strings (empty string means the slot is unused)
- `data_dir` — resolved data directory path as an absolute string

The command SHALL be read-only: it SHALL NOT mutate `settings.json` or `tasks.csv`.

#### Scenario: Outputs valid JSON
- **WHEN** `knbn config` is called
- **THEN** stdout is valid JSON containing all required top-level keys

#### Scenario: Reflects active board config
- **WHEN** `settings.json` has a custom `active_statuses` list
- **THEN** the `active_statuses` field in the JSON output matches the configured list

#### Scenario: data_dir is absolute path
- **WHEN** `knbn config` is called
- **THEN** the `data_dir` value in the JSON is an absolute filesystem path

#### Scenario: Read-only — no side effects
- **WHEN** `knbn config` is called repeatedly
- **THEN** `settings.json` and `tasks.csv` are not modified between calls
