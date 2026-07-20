# tui-board

## Purpose

Terminal UI board: Kanban layout, view switching, navigation, and interaction.

## Requirements

### Requirement: Kanban view layout
The TUI SHALL display a Kanban board with three columns (`Todo`, `Now`, `Feedback`) and three swim lane rows (`High`, `Medium`, `Low`), forming a 3×3 matrix. Columns SHALL have equal width. Column headers SHALL show the status name and the count of tasks in that column. Swim lane headers SHALL show the priority label. Archive counts (Done/Delegated/Stopped) SHALL be displayed in a footer or sidebar.

Task card titles SHALL be truncated to fit the available inner width of the card (column width minus border and padding), ensuring equal left and right margins. Cards SHALL be separated by a single border row with no additional blank lines between them.

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
The TUI SHALL provide a tabular view listing all active tasks grouped by status (`Now`, `Feedback`, `Todo`), sorted within each group by priority descending then `Last edited time` descending. Columns: `Name`, `Priority`, `Category`, `Due`. Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task detail panel.

#### Scenario: Tabular view groups by status
- **WHEN** the user switches to the Tabular view
- **THEN** tasks are grouped under `Now`, `Feedback`, and `Todo` section headers

#### Scenario: Navigate rows with arrow keys
- **WHEN** the user presses `↑` or `↓` in the Tabular view
- **THEN** focus moves to the previous or next task row and the focused row is visually highlighted

#### Scenario: Skip 10 rows with Shift+Up
- **WHEN** the user presses `Shift+↑` on a focused row in the Tabular view
- **THEN** focus moves 10 rows up, clamping at the first row

#### Scenario: Skip 10 rows with Shift+Down
- **WHEN** the user presses `Shift+↓` on a focused row in the Tabular view
- **THEN** focus moves 10 rows down, clamping at the last row

#### Scenario: Tab does nothing in Tabular view
- **WHEN** the user presses Tab or Shift+Tab in the Tabular view
- **THEN** focus does not change

#### Scenario: Auto-focus first row on mount
- **WHEN** the Tabular view is displayed
- **THEN** the first task row is immediately focused without any keypress

#### Scenario: Open detail panel from tabular view
- **WHEN** the user presses `Enter` on a focused task row in the Tabular view
- **THEN** the task detail panel opens for that task

### Requirement: Done view
The TUI SHALL provide a Done view listing terminal-status tasks (`Done`, `Delegated`, `Stopped`) grouped by ISO calendar week of `Last edited time`, most recent week first. Columns: `Name`, `Category`, `Priority`, `Last edited time`, `Date Created`. Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task detail panel.

#### Scenario: Done tasks grouped by week
- **WHEN** the user switches to the Done view
- **THEN** tasks appear under week-range headers (e.g. `Jul 12–18 2026  7`)

#### Scenario: Navigate rows with arrow keys
- **WHEN** the user presses `↑` or `↓` in the Done view
- **THEN** focus moves to the previous or next task row and the focused row is visually highlighted

#### Scenario: Skip 10 rows with Shift+Up
- **WHEN** the user presses `Shift+↑` on a focused row in the Done view
- **THEN** focus moves 10 rows up, clamping at the first row

#### Scenario: Skip 10 rows with Shift+Down
- **WHEN** the user presses `Shift+↓` on a focused row in the Done view
- **THEN** focus moves 10 rows down, clamping at the last row

#### Scenario: Tab does nothing in Done view
- **WHEN** the user presses Tab or Shift+Tab in the Done view
- **THEN** focus does not change

#### Scenario: Auto-focus first row on mount
- **WHEN** the Done view is displayed
- **THEN** the first task row is immediately focused without any keypress

#### Scenario: Open detail panel from done view
- **WHEN** the user presses `Enter` on a focused task row in the Done view
- **THEN** the task detail panel opens for that task

### Requirement: View switching
The TUI SHALL allow switching between views via keyboard: `1` for Kanban, `2` for Tabular, `3` for Done. The footer toolbar SHALL display the `q Quit` button to the left of the three view-switching buttons (`1 Kanban`, `2 Tabular`, `3 Done`).

#### Scenario: Switch to tabular view
- **WHEN** the user presses `2`
- **THEN** the Tabular view replaces the Kanban board

#### Scenario: Switch to done view
- **WHEN** the user presses `3`
- **THEN** the Done view replaces the current view

#### Scenario: Quit button appears left of view buttons
- **WHEN** the footer toolbar is rendered
- **THEN** the `q` button appears to the left of the `1`, `2`, and `3` view-switching buttons

### Requirement: Keyboard navigation on board
The TUI SHALL support arrow key navigation between cards on the Kanban board, `Enter` to open the task detail panel, `e` to edit, `d` to mark Done (with confirmation), `x` to stop, `g` to delegate, `m` to move to a different status, `p` to change priority, and `Del`/`Backspace` with confirmation to delete a task. Tab and Shift+Tab SHALL have no effect in the Kanban view. The first card in the top-left occupied cell SHALL receive focus automatically when the Kanban view is mounted. When moving left or right between columns, focus SHALL land on the card at the same row index as the current card (counting from the top of the column, ignoring swimlane boundaries), clamped to the last card if the target column has fewer cards. `PgUp`/`PgDn` SHALL reorder the focused card within its lane or move it to the adjacent priority lane. `Shift+←`/`Shift+→` SHALL move the focused card to the adjacent active status column (`Todo ↔ Now ↔ Feedback`), clamping at the boundaries; after the move the card SHALL remain focused in its new column. Terminal statuses (`Done`, `Delegated`, `Stopped`) are not reachable via Shift+arrow gestures.

#### Scenario: Arrow navigation between cards
- **WHEN** the user presses `←`/`→` on the board
- **THEN** focus moves between columns

#### Scenario: Index-preserving column switch
- **WHEN** the user is focused on the 2nd card in `Todo` and presses `←` or `→`
- **THEN** focus moves to the 2nd card in the adjacent column (counting from the top regardless of swimlane)

#### Scenario: Clamped column switch
- **WHEN** the user is focused on the 5th card in `Todo` and presses `←` to `Now` which only has 2 cards
- **THEN** focus moves to the last card (2nd) in `Now`

#### Scenario: Mark task done with confirmation
- **WHEN** the user presses `d` on a focused card
- **THEN** a confirmation dialog appears asking whether to mark the task Done

#### Scenario: Confirm done marks task
- **WHEN** the user confirms in the Done confirmation dialog
- **THEN** the task status changes to `Done` and the card disappears from the board

#### Scenario: Cancel done leaves task intact
- **WHEN** the user cancels the Done confirmation dialog
- **THEN** the task remains unchanged on the board

#### Scenario: Mark task done
- **WHEN** the user confirms `d` on a focused card
- **THEN** the task status changes to `Done` and the card disappears from the board

#### Scenario: Tab does nothing in Kanban view
- **WHEN** the user presses Tab or Shift+Tab in the Kanban view
- **THEN** focus does not change

#### Scenario: Auto-focus first card on mount
- **WHEN** the Kanban view is displayed
- **THEN** the first card in the first non-empty column is immediately focused without any keypress

#### Scenario: Shift+Up promotes priority
- **WHEN** the user presses `Shift+↑` on a focused card with priority `Medium`
- **THEN** the card's priority changes to `High`, the board refreshes, and the moved card is focused

#### Scenario: Shift+Up at top priority is a no-op
- **WHEN** the user presses `Shift+↑` on a focused card with priority `High`
- **THEN** the card is unchanged

#### Scenario: Shift+Down demotes priority
- **WHEN** the user presses `Shift+↓` on a focused card with priority `Medium`
- **THEN** the card's priority changes to `Low`, the board refreshes, and the moved card is focused

#### Scenario: Shift+Right moves card to next active status
- **WHEN** the user presses `Shift+→` on a focused card in `Todo`
- **THEN** the card moves to `Now`, the board refreshes, and the moved card is focused

#### Scenario: Shift+Left moves card to previous active status
- **WHEN** the user presses `Shift+←` on a focused card in `Now`
- **THEN** the card moves to `Todo`, the board refreshes, and the moved card is focused

#### Scenario: Shift+Right at Feedback is a no-op
- **WHEN** the user presses `Shift+→` on a focused card in `Feedback`
- **THEN** the card is unchanged and does not move to a terminal status

### Requirement: Task detail panel
The TUI SHALL display all task fields in a right-side detail panel when the user presses `Enter` on a card. The panel SHALL support `Esc`/`q` to close, `e` to edit, `n` to open notes, `o` to open the Key Resource URL in the default browser, and `d` to delete the task after confirmation.

#### Scenario: Detail panel shows all fields
- **WHEN** the user presses `Enter` on a task card
- **THEN** a panel appears showing all ten task fields

#### Scenario: Open key resource URL
- **WHEN** the user presses `o` in the detail panel and a Key Resource URL is set
- **THEN** the URL opens in the default system browser

#### Scenario: Delete task with confirmation
- **WHEN** the user presses `d` in the detail panel
- **THEN** a confirmation prompt appears asking whether to delete the task

#### Scenario: Confirm delete removes task
- **WHEN** the user confirms deletion in the prompt
- **THEN** the task is permanently removed from the store, the detail panel is dismissed, and the board refreshes

#### Scenario: Cancel delete leaves task intact
- **WHEN** the user cancels deletion in the prompt
- **THEN** the task is not deleted and the detail panel remains open

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
