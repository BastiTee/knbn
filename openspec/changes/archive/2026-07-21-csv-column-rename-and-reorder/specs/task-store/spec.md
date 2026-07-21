## MODIFIED Requirements

### Requirement: CSV schema
The store SHALL use a CSV file (`tasks.csv`) with exactly ten columns in this order: `DateTimeCreated`, `DateTimeEdited`, `DateTimeDue`, `Status`, `Priority`, `Category`, `Name`, `Delegate`, `Feedback`, `KeyResource`. The column order is canonical and must not change. On reading an existing CSV, the store SHALL validate that the header row matches the expected columns exactly (name and order); if it does not match, the store SHALL raise a `ValueError` with a message showing both the expected and the found header, before any task rows are read.

#### Scenario: Fresh init writes correct header
- **WHEN** `ensure_data_dir` is called on an empty directory
- **THEN** the created `tasks.csv` has the header `DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,Delegate,Feedback,KeyResource`

#### Scenario: Load tasks succeeds with correct schema
- **WHEN** `load_tasks` is called on a CSV with the correct header
- **THEN** tasks are returned without error

#### Scenario: Load tasks fails with wrong schema
- **WHEN** `load_tasks` is called on a CSV whose header does not match the expected columns
- **THEN** a `ValueError` is raised containing both the expected and the found header in the message

#### Scenario: Round-trip preserves all fields
- **WHEN** tasks are saved with `save_tasks` and reloaded with `load_tasks`
- **THEN** all ten task fields are identical to the originals
