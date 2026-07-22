### Requirement: Title column fills available terminal width
The table views (TabularView and ClosedView) SHALL dynamically compute the title column width so that it uses all horizontal space not occupied by the fixed columns (status, priority, category, created, edited, due date, and padding).

#### Scenario: Wide terminal
- **WHEN** the terminal width is 160 columns
- **THEN** the title column width SHALL be `max(20, 160 - FIXED_COLS_WIDTH)`, and task titles up to that length are shown untruncated

#### Scenario: Narrow terminal
- **WHEN** the terminal width is less than `FIXED_COLS_WIDTH + 20`
- **THEN** the title column width SHALL be clamped to a minimum of 20 characters

#### Scenario: Terminal resize
- **WHEN** the user resizes the terminal window while a table view is active
- **THEN** the view SHALL recompose and the title column width SHALL reflect the new width

### Requirement: Header row stays aligned with data rows
The column header row SHALL use the same `title_width` value as the data rows in the same render pass.

#### Scenario: Header alignment after resize
- **WHEN** the terminal is resized and the view recomposes
- **THEN** the header labels and data row columns SHALL remain horizontally aligned
