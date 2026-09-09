# task-model

## Purpose

Core data structures and enumerations for tasks.

## Requirements

### Requirement: Task data structure
The system SHALL represent each task as a typed dataclass with exactly eleven fields: `title`, `category`, `status`, `priority`, `date_created`, `date_modified`, `due`, `key_resource`, `free_text_1`, `free_text_2`, `free_text_3`. The fields `due`, `key_resource`, `free_text_1`, `free_text_2`, and `free_text_3` SHALL default to empty string. The `date_created` and `date_modified` fields SHALL be stored in `YYYY-MM-DD HH:MM` format. The `due` field SHALL be stored as `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` when set. The fields `free_text_1`, `free_text_2`, `free_text_3` replace the former `feedback_from` and `delegated_to` fields; their semantic meaning is determined entirely by labels in `BoardConfig.free_text_fields`.

#### Scenario: Task creation with required fields only
- **WHEN** a Task is constructed with title, category, status, priority, date_created, and date_modified
- **THEN** the task is valid and optional fields are empty strings

#### Scenario: Task creation with all fields
- **WHEN** a Task is constructed with all eleven fields populated
- **THEN** all field values are stored as provided

#### Scenario: Free-text fields default to empty
- **WHEN** a Task is constructed without free_text_1, free_text_2, or free_text_3
- **THEN** all three free-text fields are empty strings

### Requirement: Datetime format and helpers
The system SHALL define the canonical datetime formats as `YYYY-MM-DD HH:MM` for datetime values and `YYYY-MM-DD` for date-only values. The `now_str()` function SHALL return the current local time in `YYYY-MM-DD HH:MM` format. The module SHALL expose a `parse_datetime(s: str) -> tuple[datetime, bool] | None` function that recognises both the new canonical formats and the legacy `"Month DD, YYYY HH:MM AM/PM"` verbose format; the boolean in the tuple is `True` when the parsed value includes a time component. The module SHALL expose a `display_date_only(s: str) -> str` function that always returns `YYYY-MM-DD`, stripping any time component; it SHALL handle both new and legacy format inputs.

#### Scenario: now_str emits new format
- **WHEN** `now_str()` is called
- **THEN** the returned string matches the pattern `YYYY-MM-DD HH:MM` (e.g. `2026-07-21 15:45`)

#### Scenario: parse_datetime handles new datetime format
- **WHEN** `parse_datetime("2026-07-21 15:45")` is called
- **THEN** it returns a tuple of a `datetime(2026, 7, 21, 15, 45)` and `True`

#### Scenario: parse_datetime handles new date-only format
- **WHEN** `parse_datetime("2026-07-21")` is called
- **THEN** it returns a tuple of a `datetime(2026, 7, 21, 0, 0)` and `False`

#### Scenario: parse_datetime handles legacy format
- **WHEN** `parse_datetime("July 21, 2026 3:45 PM")` is called
- **THEN** it returns a tuple of a `datetime(2026, 7, 21, 15, 45)` and `True`

#### Scenario: parse_datetime returns None for unrecognised input
- **WHEN** `parse_datetime("not a date")` is called
- **THEN** it returns `None`
