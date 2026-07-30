## MODIFIED Requirements

### Requirement: Kanban view layout
The TUI SHALL display a Kanban board with three columns (`Todo`, `Now`, `Feedback`) and three swim lane rows (`High`, `Medium`, `Low`), forming a 3×3 matrix. Columns SHALL have equal width. Column headers SHALL show the status name and the count of tasks in that column. Swim lane headers SHALL show the priority label. Archive counts (Done/Delegated/Stopped) SHALL be displayed in a footer or sidebar.

Task card titles SHALL be truncated to fit the available inner width of the card (column width minus border and padding), ensuring equal left and right margins. Cards SHALL be separated by a single border row with no additional blank lines between them.

Each task card SHALL display two rows:
1. **Title row**: truncated title, indicator glyphs (`☰`/`※`), and — if a due date is set — the due date right-aligned within the card width (formatted as `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`). The title SHALL be truncated to leave space for the due date string when both are present. The due date SHALL be rendered in bold red when the task is overdue, or dimmed otherwise.
2. **Bottom row**: category colour tag only.

A card whose due date is within `deadline_warning_hours` hours of the current time (or already past) SHALL receive a CSS warning class that renders a thick warning-coloured bar on the right edge of the card (`border-right: thick $warning`). This is additive to the focus border so both indicators remain visible simultaneously.

#### Scenario: Board renders all active tasks
- **WHEN** the board is launched with tasks in multiple statuses and priorities
- **THEN** each task card appears in its correct (column, row) cell

#### Scenario: Column header shows count
- **WHEN** a column has 3 tasks
- **THEN** the column header shows the status name and the number 3

#### Scenario: Due date shown right-aligned on title row
- **WHEN** a task has a due date set and is displayed on the Kanban board
- **THEN** the due date appears right-aligned on the title row of the card

#### Scenario: No due date shown when not set
- **WHEN** a task has no due date
- **THEN** the title row shows only the title and indicator glyphs

#### Scenario: Warning border on approaching deadline
- **WHEN** a task's due date is within `deadline_warning_hours` hours of the current time
- **THEN** the card is rendered with a warning-coloured border

#### Scenario: Warning border on overdue task
- **WHEN** a task's due date is in the past
- **THEN** the card is rendered with a warning-coloured border

#### Scenario: No warning border on distant deadline
- **WHEN** a task's due date is more than `deadline_warning_hours` hours in the future
- **THEN** the card is rendered without a warning-coloured border
