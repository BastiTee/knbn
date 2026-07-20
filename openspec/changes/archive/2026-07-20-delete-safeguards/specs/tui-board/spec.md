## MODIFIED Requirements

### Requirement: Task CRUD operations
The store SHALL provide functions to add a new task (appends to CSV), update a task by index (replaces row), delete a task by index (removes row and its associated notes file), and load all tasks (returns list in file order).

#### Scenario: Add task
- **WHEN** `add_task` is called with a Task
- **THEN** the task is appended as a new row in `tasks.csv`

#### Scenario: Update task
- **WHEN** `update_task` is called with a valid index and modified Task
- **THEN** the row at that index is replaced in `tasks.csv`

#### Scenario: Delete task removes CSV row
- **WHEN** `delete_task` is called with a valid index
- **THEN** the row at that index is removed from `tasks.csv`

#### Scenario: Delete task removes notes file
- **WHEN** `delete_task` is called and the task has an associated notes file
- **THEN** the notes Markdown file under `notes/` is also deleted

#### Scenario: Delete task without notes file
- **WHEN** `delete_task` is called and no notes file exists for the task
- **THEN** the task is deleted from CSV without error

#### Scenario: Load tasks
- **WHEN** `load_tasks` is called
- **THEN** all tasks are returned as a list in the order they appear in the file

## MODIFIED Requirements

### Requirement: Keyboard navigation on board
The TUI SHALL support arrow key navigation between cards on the Kanban board, `Enter` to open the task detail panel, `e` to edit, `d` to mark Done (with confirmation), `x` to stop, `g` to delegate, `m` to move to a different status, `p` to change priority, and `Del`/`Backspace` with confirmation to delete a task. Tab and Shift+Tab SHALL have no effect in the Kanban view. The first card in the top-left occupied cell SHALL receive focus automatically when the Kanban view is mounted. When moving left or right between columns, focus SHALL land on the card at the same row index as the current card (counting from the top of the column, ignoring swimlane boundaries), clamped to the last card if the target column has fewer cards. `PgUp`/`PgDn` SHALL reorder the focused card within its lane or move it to the adjacent priority lane. `Shift+←`/`Shift+→` SHALL move the focused card to the adjacent active status column (`Todo ↔ Now ↔ Feedback`), clamping at the boundaries; after the move the card SHALL remain focused in its new column. Terminal statuses (`Done`, `Delegated`, `Stopped`) are not reachable via Shift+arrow gestures.

#### Scenario: Arrow navigation between cards
- **WHEN** the user presses `←`/`→` on the board
- **THEN** focus moves between columns

#### Scenario: Mark task done with confirmation
- **WHEN** the user presses `d` on a focused card
- **THEN** a confirmation dialog appears asking whether to mark the task Done

#### Scenario: Confirm done marks task
- **WHEN** the user confirms in the Done confirmation dialog
- **THEN** the task status changes to `Done` and the card disappears from the board

#### Scenario: Cancel done leaves task intact
- **WHEN** the user cancels the Done confirmation dialog
- **THEN** the task remains unchanged on the board

#### Scenario: Index-preserving column switch
- **WHEN** the user is focused on the 2nd card in `Todo` and presses `←` or `→`
- **THEN** focus moves to the 2nd card in the adjacent column (counting from the top regardless of swimlane)

#### Scenario: Clamped column switch
- **WHEN** the user is focused on the 5th card in `Todo` and presses `←` to `Now` which only has 2 cards
- **THEN** focus moves to the last card (2nd) in `Now`

#### Scenario: Mark task done
- **WHEN** the user confirms `d` on a focused card
- **THEN** the task status changes to `Done` and the card disappears from the board

#### Scenario: Tab does nothing in Kanban view
- **WHEN** the user presses Tab or Shift+Tab in the Kanban view
- **THEN** focus does not change

#### Scenario: Auto-focus first card on mount
- **WHEN** the Kanban view is displayed
- **THEN** the first card in the first non-empty column is immediately focused without any keypress
