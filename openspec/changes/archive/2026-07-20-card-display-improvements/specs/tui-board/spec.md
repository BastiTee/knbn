## MODIFIED Requirements

### Requirement: Kanban view layout
The TUI SHALL display a Kanban board with three columns (`Todo`, `Now`, `Feedback`) and three swim lane rows (`High`, `Medium`, `Low`), forming a 3×3 matrix. Columns SHALL have equal width. Column headers SHALL show the status name and the count of tasks in that column. Swim lane headers SHALL show the priority label. Archive counts (Done/Delegated/Stopped) SHALL be displayed in a footer or sidebar.

Task card titles SHALL be truncated to fit the available inner width of the card (column width minus border and padding), ensuring equal left and right margins. Cards SHALL be separated by a single border row with no additional blank lines between them.

#### Scenario: Board renders all active tasks
- **WHEN** the board is launched with tasks in multiple statuses and priorities
- **THEN** each task card appears in its correct (column, row) cell

#### Scenario: Column header shows count
- **WHEN** a column has 3 tasks
- **THEN** the column header shows the status name and the number 3

#### Scenario: Card title uses available width
- **WHEN** a task card is rendered in a column of width W
- **THEN** the title is truncated to fit within W minus border and padding characters, with no excess whitespace on either side

#### Scenario: Card title not truncated prematurely
- **WHEN** the terminal is wide enough that each column is wider than 30 characters
- **THEN** task titles are displayed up to the full available inner width, not capped at 30 characters

#### Scenario: Single-line gap between cards
- **WHEN** two task cards appear consecutively in the same column
- **THEN** they are separated by exactly one border row with no additional blank lines
