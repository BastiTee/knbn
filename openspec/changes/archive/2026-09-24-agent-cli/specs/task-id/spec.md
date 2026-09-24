## Purpose

Stable, short unique identifier assigned to every task, enabling reliable task lookup by headless tools and agents without depending on row order.

## ADDED Requirements

### Requirement: ID field on Task
Every task SHALL have an `id` field that is a non-empty string once the task is persisted. Newly created tasks SHALL receive an auto-generated ID before they are written to the CSV. The `id` field SHALL default to empty string when constructing a Task in memory (for backward compatibility with legacy CSV rows not yet migrated).

#### Scenario: New task gets a non-empty ID
- **WHEN** a task is created via any code path that calls `add_task`
- **THEN** the task's `id` field is a non-empty string before the row is written to CSV

#### Scenario: Legacy Task with no id is valid in memory
- **WHEN** a Task is constructed without the `id` keyword argument
- **THEN** the `id` field is an empty string and no error is raised

### Requirement: ID format
IDs SHALL be URL-safe alphanumeric strings of exactly 8 characters (lowercase letters and digits). IDs SHALL be generated with sufficient randomness that the probability of collision across a single user's task list is negligible (birthday-paradox safe up to at least 10,000 tasks).

#### Scenario: Generated ID matches format
- **WHEN** a new ID is generated
- **THEN** it is exactly 8 characters long and contains only `[a-z0-9]`

#### Scenario: IDs are unique across a run
- **WHEN** 1000 IDs are generated in a single process
- **THEN** all 1000 are distinct

### Requirement: Backward-compatible migration
The system SHALL detect legacy CSV rows that have an empty `ID` column and assign them a fresh ID on the first write operation that touches the store. The migration SHALL be transparent: after the write, all rows have non-empty IDs, and any subsequent read will return tasks with IDs.

#### Scenario: Migration fills empty IDs on first write
- **WHEN** `save_tasks` is called with a list that contains tasks whose `id` is empty
- **THEN** every task without an ID is assigned a new unique ID before the file is written

#### Scenario: Migration is idempotent
- **WHEN** `save_tasks` is called on a list where all tasks already have IDs
- **THEN** no IDs are changed

### Requirement: ID uniqueness within the store
The system SHALL guarantee that no two tasks in the same `tasks.csv` share the same ID. If a collision is detected during ID generation (extremely unlikely), the system SHALL retry generation until a unique ID is obtained.

#### Scenario: Collision during generation triggers retry
- **WHEN** `generate_id` produces a value that already exists in the current task list
- **THEN** generation is retried and the final ID is distinct from all existing IDs
