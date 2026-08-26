## MODIFIED Requirements

### Requirement: Keyboard navigation on board
The TUI SHALL support arrow key navigation between cards on the Kanban board, `Enter` to open the task edit form, `d` to mark Done (with confirmation), `x` to stop, `g` to delegate, `m` to move to a different status, `p` to change priority, `o` to open the focused card's `key_resource` URL in the default browser (no-op if no URL is set), and `Del`/`Backspace` with confirmation to delete a task. Tab and Shift+Tab SHALL have no effect in the Kanban view. The first card in the top-left occupied cell SHALL receive focus automatically when the Kanban view is mounted. When moving left or right between columns, focus SHALL land on the card at the same row index as the current card (counting from the top of the column, ignoring swimlane boundaries), clamped to the last card if the target column has fewer cards. `PgUp`/`PgDn` SHALL reorder the focused card within its lane or move it to the adjacent priority lane. `Shift+←`/`Shift+→` SHALL move the focused card to the adjacent active status column (`Todo ↔ Now ↔ Feedback`), clamping at the boundaries; after the move the card SHALL remain focused in its new column. Terminal statuses (`Done`, `Delegated`, `Stopped`) are not reachable via Shift+arrow gestures. Marking a task Done, Stopped, or Delegated SHALL update `Last edited time` to the current timestamp at the moment of confirmation.

#### Scenario: Arrow navigation between cards
- **WHEN** the user presses `←`/`→` on the board
- **THEN** focus moves between columns

#### Scenario: Index-preserving column switch
- **WHEN** the user is focused on the 2nd card in `Todo` and presses `←` or `→`
- **THEN** focus moves to the 2nd card in the adjacent column (counting from the top regardless of swimlane)

#### Scenario: Clamped column switch
- **WHEN** the user is focused on the 5th card in `Todo` and presses `←` to `Now` which only has 2 cards
- **THEN** focus moves to the last card (2nd) in `Now`

#### Scenario: Enter opens edit form from board
- **WHEN** the user presses `Enter` on a focused card on the Kanban board
- **THEN** the task edit form opens pre-populated with that task's fields

#### Scenario: Mark task done with confirmation
- **WHEN** the user presses `d` on a focused card
- **THEN** a confirmation dialog appears asking whether to mark the task Done

#### Scenario: Confirm done marks task and stamps Last edited time
- **WHEN** the user confirms in the Done confirmation dialog
- **THEN** the task status changes to `Done`, `Last edited time` is updated to now, and the card disappears from the board

#### Scenario: Cancel done leaves task intact
- **WHEN** the user cancels the Done confirmation dialog
- **THEN** the task remains unchanged on the board

#### Scenario: Mark task done
- **WHEN** the user confirms `d` on a focused card
- **THEN** the task status changes to `Done`, `Last edited time` is updated to now, and the card disappears from the board

#### Scenario: Mark task stopped stamps Last edited time
- **WHEN** the user confirms `x` on a focused card
- **THEN** the task status changes to `Stopped` and `Last edited time` is updated to now

#### Scenario: Delegate task stamps Last edited time
- **WHEN** the user confirms delegation via `g` on a focused card
- **THEN** the task status changes to `Delegated` and `Last edited time` is updated to now

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

#### Scenario: Open key resource URL from board
- **WHEN** the user presses `o` on a focused card that has a `key_resource` URL
- **THEN** the URL opens in the default system browser

#### Scenario: o key is no-op when no URL set
- **WHEN** the user presses `o` on a focused card with no `key_resource`
- **THEN** nothing happens

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
The TUI SHALL provide a Closed view (labelled `Closed` in the toolbar, accessible via key `3`) listing terminal-status tasks (`Done`, `Delegated`, `Stopped`) grouped by ISO calendar week of `Last edited time`, most recent week first. The view SHALL display a non-focusable column-header row at the top with the labels `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date` aligned to the corresponding data columns. Columns SHALL appear in this order: `Name` (28 chars), `Status` (11 chars), `Priority` (9 chars), `Category` (14 chars), `Created` (16 chars), `Edited` (16 chars), `Due Date`. Date fields SHALL be displayed using `display_date()`: showing `YYYY-MM-DD HH:MM` when a time component is present, or `YYYY-MM-DD` when only a date is stored. Week-group headers SHALL use the same background colour as Tabular view group headers (`$primary-darken-2`). Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task edit form pre-populated with that task's fields.

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

### Requirement: Inline add/edit form
The TUI SHALL provide an overlay form for creating and editing tasks, accessible via `a` (add) from any view and `Enter` on a focused task from any view (edit). The form SHALL be dismissible with `Esc`. The form SHALL be saveable with `Ctrl+S` provided the title field contains at least one non-whitespace character. The Due field label SHALL read `Due (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional)`. When saving, if the Due field is non-empty and does not match `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`, the form SHALL display an inline validation error below the Due field and SHALL NOT save the task.

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

## REMOVED Requirements

### Requirement: Task detail panel
**Reason**: Replaced by the edit form as the single task-opening surface. The detail panel provided a read-only view of task fields, which is fully covered by the pre-populated edit form opened with `Enter`. Removing it eliminates a redundant interaction layer and the `e` shortcut that duplicated `Enter`'s purpose.
**Migration**: Users who previously pressed `Enter` to view a task and then `e` to edit should now press `Enter` directly to open the edit form. The `e` shortcut is no longer available in any view.
