## MODIFIED Requirements

### Requirement: Task data structure
The system SHALL represent each task as a typed dataclass with exactly twelve fields: `id`, `title`, `category`, `status`, `priority`, `date_created`, `date_modified`, `due`, `key_resource`, `free_text_1`, `free_text_2`, `free_text_3`. The field `id` SHALL default to empty string. The fields `due`, `key_resource`, `free_text_1`, `free_text_2`, and `free_text_3` SHALL default to empty string. The `date_created` and `date_modified` fields SHALL be stored in `YYYY-MM-DD HH:MM` format. The `due` field SHALL be stored as `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` when set. The fields `free_text_1`, `free_text_2`, `free_text_3` replace the former `feedback_from` and `delegated_to` fields; their semantic meaning is determined entirely by labels in `BoardConfig.free_text_fields`.

#### Scenario: Task creation with required fields only
- **WHEN** a Task is constructed with title, category, status, priority, date_created, and date_modified
- **THEN** the task is valid, `id` defaults to empty string, and all other optional fields are empty strings

#### Scenario: Task creation with all fields
- **WHEN** a Task is constructed with all twelve fields populated
- **THEN** all field values are stored as provided

#### Scenario: Free-text fields default to empty
- **WHEN** a Task is constructed without free_text_1, free_text_2, or free_text_3
- **THEN** all three free-text fields are empty strings

#### Scenario: id defaults to empty string
- **WHEN** a Task is constructed without the `id` keyword argument
- **THEN** `task.id` is empty string and no error is raised
