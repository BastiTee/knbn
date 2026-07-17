## ADDED Requirements

### Requirement: Task data structure
The system SHALL represent each task as a typed dataclass with exactly ten fields: `title`, `category`, `status`, `priority`, `date_created`, `date_modified`, `due`, `key_resource`, `feedback_from`, `delegated_to`. Optional fields (`due`, `key_resource`, `feedback_from`, `delegated_to`) SHALL default to empty string.

#### Scenario: Task creation with required fields only
- **WHEN** a Task is constructed with title, category, status, priority, date_created, and date_modified
- **THEN** the task is valid and optional fields are empty strings

#### Scenario: Task creation with all fields
- **WHEN** a Task is constructed with all ten fields populated
- **THEN** all field values are stored as provided

### Requirement: Status enumeration
The system SHALL define exactly six status values: `Todo`, `Now`, `Feedback` (active) and `Done`, `Delegated`, `Stopped` (terminal). The constants `STATUS_ACTIVE`, `STATUS_TERMINAL`, and `STATUS_VALUES` SHALL be importable from the model module.

#### Scenario: Active statuses
- **WHEN** the `STATUS_ACTIVE` constant is accessed
- **THEN** it contains exactly `['Todo', 'Now', 'Feedback']` in that order

#### Scenario: Terminal statuses
- **WHEN** the `STATUS_TERMINAL` constant is accessed
- **THEN** it contains exactly `['Done', 'Delegated', 'Stopped']` in that order

### Requirement: Priority enumeration
The system SHALL define exactly three priority values in rank order: `High`, `Medium`, `Low`. The constant `PRIORITY_VALUES` SHALL be importable from the model module.

#### Scenario: Priority order
- **WHEN** the `PRIORITY_VALUES` constant is accessed
- **THEN** it equals `['High', 'Medium', 'Low']`

### Requirement: Default category list
The system SHALL define a default list of known categories: `People`, `Hiring`, `Strategy`, `Product`, `Engineering`, `Work Life`, `Ideas`. The constant `DEFAULT_CATEGORIES` SHALL be importable and used by the CLI and TUI as suggestions.

#### Scenario: Default categories available
- **WHEN** `DEFAULT_CATEGORIES` is accessed
- **THEN** it contains all seven predefined category strings
