## Purpose

Non-interactive task update command for scripts and agents to modify any field of an existing task by its ID.

## ADDED Requirements

### Requirement: knbn edit command
The system SHALL provide a `knbn edit <id>` subcommand that accepts a task ID as a positional argument and updates one or more fields of the matching task. At least one field flag must be provided; if none are given the command SHALL exit with a non-zero code and an error message. On success the command SHALL print `✓ Task updated: <title>` and exit with code 0. The `date_modified` field SHALL be updated to the current time automatically.

#### Scenario: Edit task title
- **WHEN** `knbn edit abc12345 --title "New title"` is called and a task with ID `abc12345` exists
- **THEN** the task's title is updated, `date_modified` is refreshed, and a confirmation is printed

#### Scenario: No field flags provided exits with error
- **WHEN** `knbn edit abc12345` is called with no field flags
- **THEN** the command exits with a non-zero code and prints a usage error

#### Scenario: Unknown ID exits with error
- **WHEN** `knbn edit xxxxxxxx` is called and no task has that ID
- **THEN** the command exits with a non-zero code and prints an error such as `Error: task 'xxxxxxxx' not found`

### Requirement: Editable fields
The `knbn edit` command SHALL support the following flags, each mapping to the corresponding task field:

- `--title TEXT`
- `--status TEXT` — value must be a valid status from the board config
- `--priority TEXT` — value must be a valid priority from the board config
- `--category TEXT` — value must be a valid category from the board config
- `--due TEXT` — value must be `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`; pass empty string to clear
- `--key-resource TEXT` — pass empty string to clear
- `--free-text-1 TEXT`
- `--free-text-2 TEXT`
- `--free-text-3 TEXT`

Fields not mentioned in the invocation SHALL remain unchanged.

#### Scenario: Edit status to valid value
- **WHEN** `knbn edit abc12345 --status Done` is called and `Done` is a configured status
- **THEN** the task status is updated to `Done`

#### Scenario: Edit status to invalid value exits with error
- **WHEN** `knbn edit abc12345 --status NotAStatus` is called
- **THEN** the command exits with a non-zero code listing the valid statuses

#### Scenario: Multiple fields updated in one call
- **WHEN** `knbn edit abc12345 --status Now --priority High` is called
- **THEN** both `status` and `priority` are updated and other fields are unchanged

#### Scenario: Clear due date with empty string
- **WHEN** `knbn edit abc12345 --due ""` is called
- **THEN** the task's `due` field is set to empty string

### Requirement: JSON output for edit
The `knbn edit` command SHALL support a `--json` flag. When set, the command SHALL print the full updated task as a JSON object instead of the human-readable confirmation.

#### Scenario: JSON output after edit
- **WHEN** `knbn edit abc12345 --title "New title" --json` is called
- **THEN** stdout is a JSON object representing the updated task with all fields including `id`
