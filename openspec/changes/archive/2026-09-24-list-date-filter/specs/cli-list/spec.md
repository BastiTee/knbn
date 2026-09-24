## MODIFIED Requirements

### Requirement: Filter flags
The `knbn list` command SHALL support the following optional filter flags. Multiple flags are ANDed together. All comparisons are case-insensitive.

- `--status TEXT` — show only tasks with this status (repeatable; OR across multiple values)
- `--priority TEXT` — show only tasks with this priority (repeatable; OR across multiple values)
- `--category TEXT` — show only tasks with this category (repeatable; OR across multiple values)
- `--all` — include tasks in terminal statuses (Done, Delegated, Stopped) in addition to active ones
- `--after DATE` — show only tasks whose `date_modified` is on or after DATE. DATE SHALL be accepted in `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` format. If DATE cannot be parsed the command SHALL exit with a non-zero code and an error message.

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

#### Scenario: --after filters by date_modified
- **WHEN** `knbn list --after 2026-09-01` is called
- **THEN** only tasks whose `date_modified` is on or after 2026-09-01 00:00 are shown

#### Scenario: --after with datetime precision
- **WHEN** `knbn list --after "2026-09-01 14:00"` is called
- **THEN** only tasks whose `date_modified` is on or after 2026-09-01 14:00 are shown

#### Scenario: --after combined with other filters
- **WHEN** `knbn list --status Now --after 2026-09-01` is called
- **THEN** only tasks that are both `Now` and modified on or after 2026-09-01 are shown

#### Scenario: --after with invalid date exits with error
- **WHEN** `knbn list --after "not-a-date"` is called
- **THEN** the command exits with a non-zero code and prints an error message

#### Scenario: --after with no matching tasks returns empty result
- **WHEN** `knbn list --after 2099-01-01` is called
- **THEN** the output is empty (human) or `[]` (JSON)
