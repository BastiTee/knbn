# cli-list

## Purpose

Headless task listing command that lets scripts and agents enumerate tasks, apply filters, and receive machine-readable output.

## Requirements

### Requirement: knbn list command
The system SHALL provide a `knbn list` subcommand that prints tasks to stdout. By default (no flags) it SHALL print all non-terminal tasks in a human-readable tabular format with columns: ID, Status, Priority, Category, Title. The output SHALL be sorted by status (in active-statuses order from board config), then by priority (High→Medium→Low), then by title.

#### Scenario: Default list shows active tasks
- **WHEN** `knbn list` is called with no flags
- **THEN** only tasks whose status is in `active_statuses` are shown, in status → priority → title order

#### Scenario: List on empty store prints nothing
- **WHEN** `knbn list` is called and `tasks.csv` has no data rows
- **THEN** the command exits with code 0 and prints nothing (or a single empty line)

### Requirement: Filter flags
The `knbn list` command SHALL support the following optional filter flags. Multiple flags are ANDed together. All comparisons are case-insensitive.

- `--status TEXT` — show only tasks with this status (repeatable; OR across multiple values)
- `--priority TEXT` — show only tasks with this priority (repeatable; OR across multiple values)
- `--category TEXT` — show only tasks with this category (repeatable; OR across multiple values)
- `--all` — include tasks in terminal statuses (Done, Delegated, Stopped) in addition to active ones

#### Scenario: Filter by status
- **WHEN** `knbn list --status Now` is called
- **THEN** only tasks with status `Now` are shown

#### Scenario: Repeatable filter is a union
- **WHEN** `knbn list --status Now --status Todo` is called
- **THEN** tasks with status `Now` OR `Todo` are shown

#### Scenario: --all includes terminal tasks
- **WHEN** `knbn list --all` is called
- **THEN** tasks with terminal statuses (e.g. `Done`) are included in the output

#### Scenario: Combined filters narrow results
- **WHEN** `knbn list --status Now --priority High` is called
- **THEN** only tasks that are both `Now` and `High` priority are shown

### Requirement: JSON output
The `knbn list` command SHALL support a `--json` flag. When set, the output SHALL be a JSON array of task objects, one per task, with all fields including `id`, `title`, `status`, `priority`, `category`, `due`, `key_resource`, `free_text_1`, `free_text_2`, `free_text_3`, `date_created`, `date_modified`. The same filter flags apply. The JSON SHALL be valid and machine-parseable (no trailing commas, no comments).

#### Scenario: JSON output is a valid array
- **WHEN** `knbn list --json` is called
- **THEN** stdout contains a valid JSON array; each element is a JSON object with the `id` field present

#### Scenario: JSON output respects filters
- **WHEN** `knbn list --status Now --json` is called
- **THEN** the JSON array contains only tasks with status `Now`

#### Scenario: JSON output for empty result is empty array
- **WHEN** `knbn list --status NonExistent --json` is called
- **THEN** stdout is `[]`
