## REMOVED Requirements

### Requirement: Mark Stopped quick action
**Reason**: `Stopped` is no longer a guaranteed status name; removing hardcoded terminal-status shortcuts is required for configurable boards.
**Migration**: Users can set any terminal status via the task edit form. The `mark_done` quick action (key `d`) provides a one-key shortcut to the configured `default_terminal_status`.

### Requirement: Mark Delegated quick action
**Reason**: `Delegated` is no longer a guaranteed status name; the `PromptModal` for capturing `delegated_to` relied on a hardcoded field that has been replaced by generic free-text fields.
**Migration**: Users who need a delegation workflow can configure a terminal status named `Delegated` and a free-text field named `Delegated To`; setting these requires the edit form.

## MODIFIED Requirements

### Requirement: Kanban view layout
The TUI SHALL display a Kanban board with one column per configured active status and one swim-lane row per configured priority, forming an N×M matrix where N is the number of active statuses (2–5) and M is the number of priorities (1–5). The leftmost column SHALL correspond to `default_active_status`. Columns SHALL have equal width. Column headers SHALL show the status name and the count of tasks in that column. Swim lane headers SHALL show the priority label. Archive counts (for all configured terminal statuses) SHALL be displayed in a footer.

Task card titles SHALL be truncated to fit the available inner width of the card. Cards SHALL be separated by a single border row with no additional blank lines between them.

Each task card SHALL display two rows:
1. **Title row**: truncated title, indicator glyphs (`☰`/`※`), and — if a due date is set — the due date right-aligned within the card width (formatted as `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`). The title SHALL be truncated to leave space for the due date string when both are present. The due date SHALL be rendered in bold red when the task is overdue, or dimmed otherwise.
2. **Bottom row**: category colour tag only.

A card whose due date is within `deadline_warning_hours` hours of the current time (or already past) SHALL receive a CSS warning class that renders a thick warning-coloured bar on the right edge.

#### Scenario: Board renders all active tasks
- **WHEN** the board is launched with tasks in multiple statuses and priorities
- **THEN** each task card appears in its correct (column, row) cell based on configured statuses and priorities

#### Scenario: Leftmost column is default active status
- **WHEN** the board is launched with `default_active_status` set to `'Sprint'`
- **THEN** the leftmost column is labelled `Sprint`

#### Scenario: Column count matches config
- **WHEN** `active_statuses` contains two entries
- **THEN** the board renders exactly two columns

#### Scenario: Swim-lane count matches config
- **WHEN** `priorities` contains two entries
- **THEN** the board renders exactly two swim-lane rows

#### Scenario: Footer lists all configured terminal statuses
- **WHEN** `terminal_statuses` is `['Done', 'Archived']`
- **THEN** the footer shows counts for both `Done` and `Archived`

#### Scenario: Warning border on approaching deadline
- **WHEN** a task's due date is within `deadline_warning_hours` hours of the current time
- **THEN** the card is rendered with a warning-coloured border

### Requirement: Mark Done quick action
The TUI SHALL provide a `mark_done` action bound to key `d` that transitions the focused task to `BoardConfig.default_terminal_status`, updates `date_modified`, persists the change, and reloads the view. A `ConfirmDialog` SHALL be shown before the transition.

#### Scenario: Mark done uses default terminal status
- **WHEN** `default_terminal_status` is `'Archived'` and the user presses `d`
- **THEN** the confirm dialog reads `'Mark "<title>" as Archived?'` and on confirmation sets status to `'Archived'`

#### Scenario: Mark done still works with legacy config
- **WHEN** `default_terminal_status` is `'Done'` (default config) and the user presses `d`
- **THEN** the task is transitioned to `Done`

### Requirement: Promote and demote priority actions
The TUI SHALL provide actions to promote (increase priority) and demote (decrease priority) a focused task's priority. The priority order SHALL be determined by `BoardConfig.priorities` (index 0 = highest). Promoting at the highest priority or demoting at the lowest SHALL be a no-op.

#### Scenario: Promote uses config priority order
- **WHEN** `priorities` is `['Critical', 'Normal', 'Low']` and a task has priority `'Normal'`
- **THEN** promoting the task sets its priority to `'Critical'`

#### Scenario: Demote at lowest is no-op
- **WHEN** a task has the last priority in `BoardConfig.priorities` and the user demotes
- **THEN** the task's priority is unchanged

### Requirement: Done week view filters by configured terminal statuses
The Done view (key `3`) SHALL display tasks whose status is any value in `BoardConfig.terminal_statuses`, grouped by ISO calendar week. It SHALL not assume specific status name strings.

#### Scenario: Done view shows all configured terminal statuses
- **WHEN** `terminal_statuses` is `['Done', 'Archived', 'Dropped']`
- **THEN** tasks with any of those three statuses appear in the Done view

### Requirement: Minimum terminal size enforcement
The TUI SHALL enforce a minimum terminal size of 100 columns × 30 rows. If the terminal is smaller, the application SHALL display the message `Terminal too small. Minimum size: 100×30.` and exit gracefully.

#### Scenario: Terminal too small
- **WHEN** the TUI is launched in a terminal narrower than 100 columns or shorter than 30 rows
- **THEN** the error message is displayed and the application exits without crashing

### Requirement: Swim lane collapsibility
Each swim lane (priority row) SHALL be collapsible. Toggling a collapsed lane SHALL hide all cards in that lane, showing only the lane header with the task count.

#### Scenario: Collapse swim lane
- **WHEN** the user presses Space or Enter on a focused lane header
- **THEN** the lane collapses and only the header with task count is visible

#### Scenario: Expand swim lane
- **WHEN** a collapsed lane header is focused and the user presses Space or Enter
- **THEN** the lane expands and all cards are visible again
