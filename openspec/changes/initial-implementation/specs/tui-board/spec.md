## ADDED Requirements

### Requirement: Kanban view layout
The TUI SHALL display a Kanban board with three columns (`Todo`, `Now`, `Feedback`) and three swim lane rows (`High`, `Medium`, `Low`), forming a 3×3 matrix. Columns SHALL have equal width. Column headers SHALL show the status name and the count of tasks in that column. Swim lane headers SHALL show the priority label. Archive counts (Done/Delegated/Stopped) SHALL be displayed in a footer or sidebar.

#### Scenario: Board renders all active tasks
- **WHEN** the board is launched with tasks in multiple statuses and priorities
- **THEN** each task card appears in its correct (column, row) cell

#### Scenario: Column header shows count
- **WHEN** a column has 3 tasks
- **THEN** the column header shows the status name and the number 3

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

### Requirement: Tabular view
The TUI SHALL provide a tabular view listing all active tasks grouped by status (`Now`, `Feedback`, `Todo`), sorted within each group by priority descending then `Last edited time` descending. Columns: `Name`, `Priority`, `Category`, `Due`.

#### Scenario: Tabular view groups by status
- **WHEN** the user switches to the Tabular view
- **THEN** tasks are grouped under `Now`, `Feedback`, and `Todo` section headers

### Requirement: Done-by-week view
The TUI SHALL provide a Done-by-week view listing terminal-status tasks (`Done`, `Delegated`, `Stopped`) grouped by ISO calendar week of `Last edited time`, most recent week first. Columns: `Name`, `Category`, `Priority`, `Last edited time`, `Date Created`.

#### Scenario: Done tasks grouped by week
- **WHEN** the user switches to the Done-by-week view
- **THEN** tasks appear under week-range headers (e.g. `Jul 12–18 2026  7`)

### Requirement: View switching
The TUI SHALL allow switching between views via keyboard: `1` for Kanban, `2` for Tabular, `3` for Done-by-Week.

#### Scenario: Switch to tabular view
- **WHEN** the user presses `2`
- **THEN** the Tabular view replaces the Kanban board

### Requirement: Keyboard navigation on board
The TUI SHALL support arrow key navigation between cards on the Kanban board, `Enter` to open the task detail panel, `e` to edit, `d` to mark done, `x` to stop, `g` to delegate, `m` to move to a different status, `p` to change priority, and `Del`/`Backspace` with confirmation to delete a task.

#### Scenario: Arrow navigation between cards
- **WHEN** the user presses `←`/`→` on the board
- **THEN** focus moves between columns

#### Scenario: Mark task done
- **WHEN** the user presses `d` on a focused card
- **THEN** the task status changes to `Done` and the card disappears from the board

### Requirement: Task detail panel
The TUI SHALL display all task fields in a right-side detail panel when the user presses `Enter` on a card. The panel SHALL support `Esc`/`q` to close, `e` to edit, `n` to open notes, and `o` to open the Key Resource URL in the default browser.

#### Scenario: Detail panel shows all fields
- **WHEN** the user presses `Enter` on a task card
- **THEN** a panel appears showing all ten task fields

#### Scenario: Open key resource URL
- **WHEN** the user presses `o` in the detail panel and a Key Resource URL is set
- **THEN** the URL opens in the default system browser

### Requirement: Inline add/edit form
The TUI SHALL provide an overlay form for creating and editing tasks, accessible via `a` (add) from any view and `e` from a focused card or detail panel. The form SHALL be dismissible with `Esc`.

#### Scenario: Open add form
- **WHEN** the user presses `a`
- **THEN** an overlay form appears with empty fields ready for input

#### Scenario: Cancel form
- **WHEN** the user presses `Esc` while the form is open
- **THEN** the form closes without saving any changes

### Requirement: Help overlay
The TUI SHALL display a key bindings help overlay when the user presses `?`, and dismiss it with `Esc` or `?`.

#### Scenario: Show help
- **WHEN** the user presses `?`
- **THEN** a help overlay listing all key bindings appears

### Requirement: Global quit
The TUI SHALL quit cleanly when the user presses `q` or `Ctrl+C` from any view.

#### Scenario: Quit with q
- **WHEN** the user presses `q` (not in a text input field)
- **THEN** the TUI exits and the terminal is restored to its prior state
