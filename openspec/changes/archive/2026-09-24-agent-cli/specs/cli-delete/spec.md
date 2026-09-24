## Purpose

Non-interactive task deletion command for scripts and agents to remove a task and its associated notes by ID.

## ADDED Requirements

### Requirement: knbn delete command
The system SHALL provide a `knbn delete <id>` subcommand that accepts a task ID as a positional argument and permanently removes the matching task from `tasks.csv`. If the task has an associated notes file it SHALL also be deleted. On success the command SHALL print `✓ Task deleted: <title>` and exit with code 0.

#### Scenario: Delete existing task
- **WHEN** `knbn delete abc12345` is called and a task with ID `abc12345` exists
- **THEN** the task row is removed from `tasks.csv`, any associated notes file is deleted, and a confirmation is printed

#### Scenario: Delete task without notes file
- **WHEN** `knbn delete abc12345` is called and the task has no notes file
- **THEN** the task is deleted from `tasks.csv` without error

#### Scenario: Unknown ID exits with error
- **WHEN** `knbn delete xxxxxxxx` is called and no task has that ID
- **THEN** the command exits with a non-zero code and prints an error such as `Error: task 'xxxxxxxx' not found`

### Requirement: Confirmation prompt
By default the `knbn delete` command SHALL prompt the user for confirmation before deleting (`Delete task "<title>"? [y/N]`). A `--yes` / `-y` flag SHALL skip the confirmation prompt (for non-interactive / scripted use).

#### Scenario: Confirmation prompt shown by default
- **WHEN** `knbn delete abc12345` is called interactively without `--yes`
- **THEN** a confirmation prompt is shown; answering `n` aborts with exit code 0 and no changes

#### Scenario: --yes skips confirmation
- **WHEN** `knbn delete abc12345 --yes` is called
- **THEN** the task is deleted immediately without prompting
