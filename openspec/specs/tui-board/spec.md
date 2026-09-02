# tui-board

## Purpose

Terminal UI board: Kanban layout, view switching, navigation, and interaction.

## Requirements

### Requirement: Kanban view layout
The TUI SHALL display a Kanban board with one column per configured active status and one swim-lane row per configured priority, forming an N×M matrix where N is the number of active statuses (2–5) and M is the number of priorities (1–5). The leftmost column SHALL correspond to `default_active_status`. Columns SHALL have equal width. Column headers SHALL show the status name and the count of tasks in that column. Swim lane headers SHALL show the priority label. Archive counts (for all configured terminal statuses) SHALL be displayed in a footer.

Task card titles SHALL be truncated to fit the available inner width of the card. Cards SHALL be separated by a single border row with no additional blank lines between them.

Each task card SHALL display two rows:
1. **Title row**: truncated title, indicator glyphs (`☰`/`※`), and — if a due date is set — the due date right-aligned within the card width (formatted as `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`). The title SHALL be truncated to leave space for the due date string when both are present. The due date SHALL be rendered in bold red when the task is overdue, or dimmed otherwise.
2. **Bottom row**: category colour tag only.

A card whose due date is within `deadline_warning_hours` hours of the current time (or already past) SHALL receive a CSS warning class that renders a thick warning-coloured bar on the right edge of the card (`border-right: thick $warning`). This is additive to the focus border so both indicators remain visible simultaneously.

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
The TUI SHALL provide a tabular view listing all active tasks grouped by status (`Now`, `Feedback`, `Todo`), sorted within each group by priority descending then `Last edited time` descending. The view SHALL display a non-focusable column-header row at the top with the labels `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date` aligned to the corresponding data columns. Columns SHALL appear in this order: `Name` (28 chars), `Status` (11 chars), `Priority` (9 chars), `Category` (14 chars), `Created` (16 chars), `Edited` (16 chars), `Due Date`. Date fields SHALL be displayed using `display_date()`: showing `YYYY-MM-DD HH:MM` when a time component is present in the stored value, or `YYYY-MM-DD` when only a date is stored. Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task edit form pre-populated with that task's fields.

#### Scenario: Tabular view shows column headers
- **WHEN** the user switches to the Tabular view
- **THEN** a non-focusable header row appears at the top showing `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date`

#### Scenario: Date-only value shown without time
- **WHEN** a task has a `date_modified` of `2026-07-21` (no time component)
- **THEN** the Edited column shows `2026-07-21`

#### Scenario: Datetime value shown with time
- **WHEN** a task has a `date_modified` of `2026-07-21 15:45`
- **THEN** the Edited column shows `2026-07-21 15:45`

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

#### Scenario: Enter opens edit form from tabular view
- **WHEN** the user presses `Enter` on a focused task row in the Tabular view
- **THEN** the task edit form opens pre-populated with that task's fields

### Requirement: Closed view
The TUI SHALL provide a Closed view (labelled `Closed` in the toolbar, accessible via key `3`) listing tasks whose status is any value in `BoardConfig.terminal_statuses`, grouped by ISO calendar week of `Last edited time`, most recent week first. The view SHALL NOT assume specific status name strings. The view SHALL display a non-focusable column-header row at the top with the labels `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date` aligned to the corresponding data columns. Columns SHALL appear in this order: `Name` (28 chars), `Status` (11 chars), `Priority` (9 chars), `Category` (14 chars), `Created` (16 chars), `Edited` (16 chars), `Due Date`. Date fields SHALL be displayed using `display_date()`: showing `YYYY-MM-DD HH:MM` when a time component is present, or `YYYY-MM-DD` when only a date is stored. Week-group headers SHALL use the same background colour as Tabular view group headers (`$primary-darken-2`). Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task edit form pre-populated with that task's fields.

#### Scenario: Done view shows all configured terminal statuses
- **WHEN** `terminal_statuses` is `['Done', 'Archived', 'Dropped']`
- **THEN** tasks with any of those three statuses appear in the Done view

#### Scenario: Closed view shows column headers
- **WHEN** the user switches to the Closed view
- **THEN** a non-focusable header row appears at the top showing `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date`

#### Scenario: Closed tasks grouped by week
- **WHEN** the user switches to the Closed view
- **THEN** tasks appear under week-range headers (e.g. `Jul 12–18 2026  7`)

#### Scenario: Row shows task status
- **WHEN** a Delegated task appears in the Closed view
- **THEN** the row displays `Delegated` in the Status column

#### Scenario: Week headers use primary colour
- **WHEN** the Closed view is displayed
- **THEN** week-group header backgrounds match the Tabular view group-header style

#### Scenario: Navigate rows with arrow keys
- **WHEN** the user presses `↑` or `↓` in the Closed view
- **THEN** focus moves to the previous or next task row and the focused row is visually highlighted

#### Scenario: Skip 10 rows with Shift+Up
- **WHEN** the user presses `Shift+↑` on a focused row in the Closed view
- **THEN** focus moves 10 rows up, clamping at the first row

#### Scenario: Skip 10 rows with Shift+Down
- **WHEN** the user presses `Shift+↓` on a focused row in the Closed view
- **THEN** focus moves 10 rows down, clamping at the last row

#### Scenario: Tab does nothing in Closed view
- **WHEN** the user presses Tab or Shift+Tab in the Closed view
- **THEN** focus does not change

#### Scenario: Auto-focus first row on mount
- **WHEN** the Closed view is displayed
- **THEN** the first task row is immediately focused without any keypress

#### Scenario: Enter opens edit form from closed view
- **WHEN** the user presses `Enter` on a focused task row in the Closed view
- **THEN** the task edit form opens pre-populated with that task's fields

### Requirement: View switching
The TUI SHALL allow switching between views via keyboard: `1` for Kanban, `2` for Tabular, `3` for Closed. The footer toolbar SHALL display the `q Quit` button to the left of the three view-switching buttons (`1 Kanban`, `2 Tabular`, `3 Closed`). The footer SHALL visually indicate which view is currently active by rendering the corresponding tab key in bold.

#### Scenario: Switch to tabular view
- **WHEN** the user presses `2`
- **THEN** the Tabular view replaces the Kanban board

#### Scenario: Switch to closed view
- **WHEN** the user presses `3`
- **THEN** the Closed view replaces the current view

#### Scenario: Quit button appears left of view buttons
- **WHEN** the footer toolbar is rendered
- **THEN** the `q` button appears to the left of the `1`, `2`, and `3` view-switching buttons

#### Scenario: Active tab key is highlighted in footer
- **WHEN** a view is active
- **THEN** the corresponding tab key (`1`, `2`, or `3`) in the footer is rendered in bold to indicate the active view

### Requirement: Keyboard navigation on board
The TUI SHALL support arrow key navigation between cards on the Kanban board, `Enter` to open the task edit form, `d` to mark done (with confirmation), `m` to move to a different status, `p` to change priority, `o` to open the focused card's `key_resource` URL in the default browser (no-op if no URL is set), and `Del`/`Backspace` with confirmation to delete a task. Tab and Shift+Tab SHALL have no effect in the Kanban view. The first focusable element (card or, if the column is empty, its first lane header) in the first column SHALL receive focus automatically when the Kanban view is mounted. When moving left or right between columns, focus SHALL land on the card at the same row index as the current card (counting from the top of the column, ignoring swimlane boundaries), clamped to the last card if the target column has fewer cards. If the target column has no cards at all, focus SHALL land on the topmost visible `LaneHeader` in that column. `PgUp`/`PgDn` SHALL reorder the focused card within its lane or move it to the adjacent priority lane. `Shift+←`/`Shift+→` SHALL move the focused card to the adjacent active status column, clamping at the boundaries; after the move the card SHALL remain focused in its new column. Terminal statuses are not reachable via Shift+arrow gestures. Marking a task via the mark-done quick action SHALL update `Last edited time` to the current timestamp at the moment of confirmation.

#### Scenario: Arrow navigation between cards
- **WHEN** the user presses `←`/`→` on the board
- **THEN** focus moves between columns

#### Scenario: Index-preserving column switch
- **WHEN** the user is focused on the 2nd card in `Todo` and presses `←` or `→`
- **THEN** focus moves to the 2nd card in the adjacent column (counting from the top regardless of swimlane)

#### Scenario: Clamped column switch
- **WHEN** the user is focused on the 5th card in `Todo` and presses `←` to `Now` which only has 2 cards
- **THEN** focus moves to the last card (2nd) in `Now`

#### Scenario: Navigate into empty column focuses lane header
- **WHEN** the user presses `←` or `→` and the target column has no task cards
- **THEN** focus moves to the topmost visible `LaneHeader` in that column

#### Scenario: Enter opens edit form from board
- **WHEN** the user presses `Enter` on a focused card on the Kanban board
- **THEN** the task edit form opens pre-populated with that task's fields

#### Scenario: Mark task done with confirmation
- **WHEN** the user presses `d` on a focused card
- **THEN** a confirmation dialog appears asking whether to mark the task Done

#### Scenario: Confirm done marks task and stamps Last edited time
- **WHEN** the user confirms in the done confirmation dialog
- **THEN** the task status changes to the configured default terminal status, `Last edited time` is updated to now, and the card disappears from the board

#### Scenario: Cancel done leaves task intact
- **WHEN** the user cancels the done confirmation dialog
- **THEN** the task remains unchanged on the board

#### Scenario: Mark task done
- **WHEN** the user confirms `d` on a focused card
- **THEN** the task status changes to the configured default terminal status, `Last edited time` is updated to now, and the card disappears from the board

#### Scenario: Tab does nothing in Kanban view
- **WHEN** the user presses Tab or Shift+Tab in the Kanban view
- **THEN** focus does not change

#### Scenario: Auto-focus first card on mount
- **WHEN** the Kanban view is displayed
- **THEN** the first focusable element (card or lane header) in the first column is immediately focused without any keypress

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

#### Scenario: Open key resource URL from board
- **WHEN** the user presses `o` on a focused card that has a `key_resource` URL
- **THEN** the URL opens in the default system browser

#### Scenario: o key is no-op when no URL set
- **WHEN** the user presses `o` on a focused card with no `key_resource`
- **THEN** nothing happens

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

### Requirement: Inline add/edit form
The TUI SHALL provide an overlay form for creating and editing tasks, accessible via `a` (add) from any view and `Enter` on a focused task from any view (edit). The form SHALL be dismissible with `Esc`. The form SHALL be saveable with `Ctrl+S` provided the title field contains at least one non-whitespace character. The Due field label SHALL read `Due (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional)`. When saving, if the Due field is non-empty and does not match `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`, the form SHALL display an inline validation error below the Due field and SHALL NOT save the task. The Due field SHALL additionally apply a red border highlight (CSS class `--invalid`) when its value fails validation; this highlight SHALL be cleared when the user begins editing the field again.

When `a` is pressed from the Kanban view, the add form SHALL pre-populate the Status and Priority fields based on the currently focused cell: Status from the focused column (`Todo`, `Now`, or `Feedback`) and Priority from the focused swim lane row (`High`, `Medium`, or `Low`). If lane context cannot be determined, the form SHALL fall back to the default values (`Todo` / `Medium`). Pre-populated values SHALL remain editable by the user.

Pressing `Enter` while the Due field is focused SHALL open the `DateTimePicker` overlay instead of submitting the form, subject to the following rules:
- If the Due field is empty, the picker opens with today's date selected and an empty time input.
- If the Due field contains a valid `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` value, the picker opens pre-filled with that value.
- If the Due field contains an invalid value, the validation error is shown (with the `--invalid` highlight) and the picker does NOT open.
On picker confirmation, the returned value is written into the Due field. On picker cancellation, the Due field is unchanged.

#### Scenario: Open add form
- **WHEN** the user presses `a`
- **THEN** an overlay form appears with empty fields ready for input

#### Scenario: Open edit form from any view
- **WHEN** the user presses `Enter` on a focused task in any view
- **THEN** an overlay form appears pre-populated with that task's current field values

#### Scenario: Cancel form with Escape
- **WHEN** the user presses `Esc` while the form is open
- **THEN** the form closes without saving any changes

#### Scenario: Save form with Ctrl+S
- **WHEN** the user presses `Ctrl+S` while the form is open and the title field has at least one character
- **THEN** the task is saved and the form closes

#### Scenario: Ctrl+S ignored when title is empty
- **WHEN** the user presses `Ctrl+S` while the title field is empty or whitespace-only
- **THEN** the form remains open and nothing is saved

#### Scenario: Valid date-only due accepted
- **WHEN** the user enters `2026-08-01` in the Due field and saves
- **THEN** the task is saved with `due = "2026-08-01"`

#### Scenario: Valid datetime due accepted
- **WHEN** the user enters `2026-08-01 09:00` in the Due field and saves
- **THEN** the task is saved with `due = "2026-08-01 09:00"`

#### Scenario: Invalid due format blocked
- **WHEN** the user enters `01/08/2026` in the Due field and attempts to save
- **THEN** an inline error message appears below the Due field and the task is not saved

#### Scenario: Invalid due field gets red border
- **WHEN** validation fails on the Due field (on save attempt or on Enter when invalid)
- **THEN** the Due field border turns red via the `--invalid` CSS class

#### Scenario: Red border cleared on edit
- **WHEN** the user starts typing in the Due field after a validation error
- **THEN** the `--invalid` CSS class is removed and the border returns to normal

#### Scenario: Enter on empty Due field opens picker
- **WHEN** the Due field is empty and the user presses `Enter` while it is focused
- **THEN** the `DateTimePicker` overlay opens with today's date selected

#### Scenario: Enter on valid Due field opens picker pre-filled
- **WHEN** the Due field contains `2026-09-15` and the user presses `Enter` while it is focused
- **THEN** the `DateTimePicker` overlay opens with September 2026 showing and the 15th selected

#### Scenario: Enter on invalid Due field shows error, no picker
- **WHEN** the Due field contains `not-a-date` and the user presses `Enter` while it is focused
- **THEN** the validation error and red border are shown and the picker does NOT open

#### Scenario: Picker confirmation writes value to Due field
- **WHEN** the user confirms a date of `2026-10-01` in the picker
- **THEN** the Due field is updated to `2026-10-01` and the picker closes

#### Scenario: Picker cancellation leaves Due field unchanged
- **WHEN** the user presses `Esc` in the picker
- **THEN** the Due field retains its previous value

#### Scenario: Add form pre-populates status from focused column
- **WHEN** the user is focused on a card or lane header in the `Feedback` column of the Kanban board and presses `a`
- **THEN** the add form opens with Status pre-set to `Feedback`

#### Scenario: Add form pre-populates priority from focused swim lane
- **WHEN** the user is focused on a card or lane header in the `High` swim lane of the Kanban board and presses `a`
- **THEN** the add form opens with Priority pre-set to `High`

#### Scenario: Add form pre-population from focused card
- **WHEN** the user is focused on a card in the `Now` column / `Low` swim lane and presses `a`
- **THEN** the add form opens with Status pre-set to `Now` and Priority pre-set to `Low`

#### Scenario: Add form falls back to defaults when no lane context
- **WHEN** the user presses `a` from the Tabular or Closed view
- **THEN** the add form opens with the default Status (`Todo`) and Priority (`Medium`)

### Requirement: Help overlay
The TUI SHALL display a key bindings help overlay when the user presses `?`, and dismiss it with `Esc` or `?`.

#### Scenario: Show help
- **WHEN** the user presses `?`
- **THEN** a help overlay listing all key bindings appears

### Requirement: Global quit
The TUI SHALL quit cleanly when the user presses `q` or `Ctrl+C` from any view. There is no dedicated Reload keybinding.

#### Scenario: Quit with q
- **WHEN** the user presses `q` (not in a text input field)
- **THEN** the TUI exits and the terminal is restored to its prior state

### Requirement: Command palette
The TUI SHALL expose a command palette via `Ctrl+P`. The palette SHALL contain exactly the following commands in order: `Theme`, `Quit`, `Keys`. The `Screenshot` and `Maximize`/`Minimize` commands SHALL NOT appear in the palette. The application SHALL NOT display a title header bar; no mouse-clickable palette trigger SHALL be present.

#### Scenario: Palette shows Theme then Quit
- **WHEN** the user opens the command palette with `Ctrl+P`
- **THEN** the first entry is `Theme` and the second entry is `Quit`

#### Scenario: Screenshot absent from palette
- **WHEN** the user opens the command palette
- **THEN** no `Screenshot` command is listed

#### Scenario: Maximize absent from palette
- **WHEN** the user opens the command palette
- **THEN** no `Maximize` or `Minimize` command is listed

#### Scenario: No title header bar rendered
- **WHEN** the TUI is launched
- **THEN** no header bar is displayed at the top of the screen
