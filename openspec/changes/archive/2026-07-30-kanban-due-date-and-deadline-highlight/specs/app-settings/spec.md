## ADDED Requirements

### Requirement: Deadline warning hours setting
The system SHALL support a `deadline_warning_hours` setting whose value is a positive integer (stored as a string). It controls how many hours before a task's due date the Kanban card warning highlight is shown. The default value SHALL be `24`. If the stored value is not a valid positive integer, the system SHALL silently fall back to `24`.

#### Scenario: Default deadline_warning_hours is 24
- **WHEN** no `settings.json` exists or the `deadline_warning_hours` key is absent
- **THEN** the deadline warning window is 24 hours

#### Scenario: Custom deadline_warning_hours applied
- **WHEN** `settings.json` contains `{"deadline_warning_hours": "48"}`
- **THEN** the deadline warning highlight appears on cards with a due date within 48 hours

#### Scenario: Invalid value falls back to default
- **WHEN** `settings.json` contains `{"deadline_warning_hours": "bad"}`
- **THEN** the deadline warning window falls back to 24 hours
