## MODIFIED Requirements

### Requirement: Title column fills available terminal width
The table views (TabularView and ClosedView) SHALL dynamically compute the title column width so that it uses all horizontal space not occupied by the fixed columns (status, priority, category, created, edited, due, and padding).

#### Scenario: Wide terminal
- **WHEN** the terminal width is 160 columns
- **THEN** the title column width SHALL be `max(20, 160 - FIXED_COLS_WIDTH)`, and task titles up to that length are shown untruncated

#### Scenario: Narrow terminal
- **WHEN** the terminal width is less than `FIXED_COLS_WIDTH + 20`
- **THEN** the title column width SHALL be clamped to a minimum of 20 characters

#### Scenario: Terminal resize
- **WHEN** the user resizes the terminal window while a table view is active
- **THEN** the view SHALL recompose and the title column width SHALL reflect the new width

## ADDED Requirements

### Requirement: Date columns display date only, no time
The Created, Edited, and Due columns in table views SHALL display only the date portion (`YYYY-MM-DD`), regardless of whether a time component is stored in the underlying value.

#### Scenario: Datetime value with time component
- **WHEN** a task's created, edited, or due value contains a time component (e.g., `2024-03-15T09:30:00`)
- **THEN** the column SHALL render `2024-03-15` and SHALL NOT show the time part

#### Scenario: Date-only value
- **WHEN** a task's created, edited, or due value contains no time component
- **THEN** the column SHALL render the date as `YYYY-MM-DD`

### Requirement: Due column header label is "Due"
The header label for the due-date column SHALL be `Due`, not `Due Date`.

#### Scenario: Header row in table view
- **WHEN** the user opens the Tabular or Closed (done_week) view
- **THEN** the column header row SHALL show `Due` as the label for the due-date column
