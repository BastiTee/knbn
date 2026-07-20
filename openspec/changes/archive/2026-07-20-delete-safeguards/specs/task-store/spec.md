## MODIFIED Requirements

### Requirement: Task CRUD operations
The store SHALL provide functions to add a new task (appends to CSV), update a task by index (replaces row), delete a task by index (removes row and its associated notes file), and load all tasks (returns list in file order).

#### Scenario: Add task
- **WHEN** `add_task` is called with a Task
- **THEN** the task is appended as a new row in `tasks.csv`

#### Scenario: Update task
- **WHEN** `update_task` is called with a valid index and modified Task
- **THEN** the row at that index is replaced in `tasks.csv`

#### Scenario: Delete task removes CSV row
- **WHEN** `delete_task` is called with a valid index
- **THEN** the row at that index is removed from `tasks.csv`

#### Scenario: Delete task removes notes file
- **WHEN** `delete_task` is called and the task has an associated notes file
- **THEN** the notes Markdown file under `notes/` is also deleted

#### Scenario: Delete task without notes file
- **WHEN** `delete_task` is called and no notes file exists for the task
- **THEN** the task is deleted from CSV without error

#### Scenario: Load tasks
- **WHEN** `load_tasks` is called
- **THEN** all tasks are returned as a list in the order they appear in the file
