## MODIFIED Requirements

### Requirement: CSV schema
The store SHALL use a CSV file (`tasks.csv`) with exactly twelve columns in this order: `ID`, `DateTimeCreated`, `DateTimeEdited`, `DateTimeDue`, `Status`, `Priority`, `Category`, `Name`, `FreeText1`, `FreeText2`, `FreeText3`, `KeyResource`. The column order is canonical and must not change. On reading an existing CSV, the store SHALL validate that the header row matches the expected columns exactly (name and order); if it does not match, the store SHALL raise a `ValueError` with a message showing both the expected and the found header, before any task rows are read.

#### Scenario: Fresh init writes correct header
- **WHEN** `ensure_data_dir` is called on an empty directory
- **THEN** the created `tasks.csv` has the header `ID,DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,FreeText1,FreeText2,FreeText3,KeyResource`

#### Scenario: Load tasks succeeds with correct schema
- **WHEN** `load_tasks` is called on a CSV with the correct 12-column header
- **THEN** tasks are returned without error

#### Scenario: Load tasks fails with wrong schema
- **WHEN** `load_tasks` is called on a CSV whose header does not match the expected columns
- **THEN** a `ValueError` is raised containing both the expected and the found header in the message

#### Scenario: Round-trip preserves all fields
- **WHEN** tasks are saved with `save_tasks` and reloaded with `load_tasks`
- **THEN** all task fields are identical to the originals

#### Scenario: Round-trip preserves all fields including ID
- **WHEN** tasks with non-empty `id` values are saved with `save_tasks` and reloaded with `load_tasks`
- **THEN** all twelve task fields, including `id`, are identical to the originals

### Requirement: Task CRUD operations
The store SHALL provide functions to add a new task (appends to CSV), update a task by ID (replaces row), delete a task by ID (removes row and its associated notes file), and load all tasks (returns list in file order). Index-based overloads are deprecated; all external callers SHALL use ID-based lookups.

#### Scenario: Add task
- **WHEN** `add_task` is called with a Task
- **THEN** the task is appended as a new row in `tasks.csv` with a non-empty `ID` value

#### Scenario: Update task
- **WHEN** `update_task` is called with a valid index and modified Task
- **THEN** the row at that index is replaced in `tasks.csv`

#### Scenario: Update task by ID
- **WHEN** `update_task_by_id` is called with a valid task ID and a modified Task
- **THEN** the matching row is replaced in `tasks.csv`

#### Scenario: Update task by unknown ID raises error
- **WHEN** `update_task_by_id` is called with an ID that does not exist in `tasks.csv`
- **THEN** a `TaskNotFoundError` is raised

#### Scenario: Delete task removes CSV row
- **WHEN** `delete_task` is called with a valid index
- **THEN** the row at that index is removed from `tasks.csv`

#### Scenario: Delete task by ID removes CSV row
- **WHEN** `delete_task_by_id` is called with a valid task ID
- **THEN** the matching row is removed from `tasks.csv`

#### Scenario: Delete task by unknown ID raises error
- **WHEN** `delete_task_by_id` is called with an ID that does not exist
- **THEN** a `TaskNotFoundError` is raised

#### Scenario: Delete task removes notes file
- **WHEN** `delete_task` is called and the task has an associated notes file
- **THEN** the notes Markdown file under `notes/` is also deleted

#### Scenario: Delete task without notes file
- **WHEN** `delete_task` is called and no notes file exists for the task
- **THEN** the task is deleted from CSV without error

#### Scenario: Delete task by ID removes notes file
- **WHEN** `delete_task_by_id` is called and the task has an associated notes file
- **THEN** the notes Markdown file under `notes/` is also deleted

#### Scenario: Load tasks
- **WHEN** `load_tasks` is called
- **THEN** all tasks are returned as a list in the order they appear in the file

### Requirement: find_task_by_id
The store SHALL expose a `find_task_by_id(data_dir, task_id) -> Task` function that loads all tasks and returns the first task whose `id` matches exactly. If no task is found it SHALL raise `TaskNotFoundError`.

#### Scenario: Find existing task
- **WHEN** `find_task_by_id` is called with an ID that exists in `tasks.csv`
- **THEN** the matching Task is returned

#### Scenario: Find non-existent task raises error
- **WHEN** `find_task_by_id` is called with an ID that does not exist
- **THEN** `TaskNotFoundError` is raised

## ADDED Requirements

### Requirement: TaskNotFoundError
The store module SHALL define a `TaskNotFoundError` exception class (subclass of `ValueError`) raised when a task lookup by ID fails.

#### Scenario: TaskNotFoundError is raised on missing ID
- **WHEN** any by-ID store function is called with an unknown ID
- **THEN** `TaskNotFoundError` is raised with a message containing the unknown ID
