## Purpose

Live substring filter that hides non-matching tasks across all three TUI views, activated and dismissed entirely from the keyboard.

## ADDED Requirements

### Requirement: Search activation and deactivation
The system SHALL activate the search filter when the user presses `Ctrl+F`. Activation SHALL show a one-line search bar above the footer displaying the current query. The search SHALL be deactivated when the user presses `Esc`, which clears the query and restores all tasks. Pressing `Ctrl+F` again while search is active SHALL also deactivate it.

#### Scenario: Ctrl+F shows search bar
- **WHEN** the user presses `Ctrl+F`
- **THEN** a search bar row appears above the footer displaying an empty query prompt

#### Scenario: Esc clears and hides search bar
- **WHEN** the search is active and the user presses `Esc`
- **THEN** the search bar disappears and all tasks become visible again

#### Scenario: Ctrl+F again deactivates
- **WHEN** the search is active and the user presses `Ctrl+F` again
- **THEN** the search bar disappears and all tasks become visible again

### Requirement: Search bar display
The search bar SHALL appear as a one-line row positioned above the footer (status bar). It SHALL show a `/` prefix followed by the current query text and a cursor indicator. When no search is active the row SHALL be hidden (zero height, not occupying layout space).

#### Scenario: Search bar shows query
- **WHEN** the search is active and the user has typed `work`
- **THEN** the search bar displays `/ work▋`

#### Scenario: Search bar hidden when inactive
- **WHEN** the search is not active
- **THEN** no additional row is visible above the footer

### Requirement: Live filtering
As the user types, the system SHALL hide tasks that do not match the current query and show only matching tasks. The filter SHALL be case-insensitive and match any substring of the task's title, category, or any of the three free-text fields (`free_text_1`, `free_text_2`, `free_text_3`). A task matches if the query appears in ANY of those fields.

#### Scenario: Title match
- **WHEN** the query is `bug`
- **THEN** tasks whose title contains `bug` (case-insensitively) are shown

#### Scenario: Category match
- **WHEN** the query is `work`
- **THEN** tasks whose category contains `work` are shown

#### Scenario: Free-text field match
- **WHEN** the query is `alice`
- **THEN** tasks where any of free_text_1/2/3 contains `alice` are shown

#### Scenario: No match hides task
- **WHEN** the query does not match title, category, or any free-text field of a task
- **THEN** that task is hidden from the current view

#### Scenario: Empty query shows all tasks
- **WHEN** the search is active but the query is empty
- **THEN** all tasks are visible (same as no filter)

### Requirement: Filter applies to all three views
The search filter SHALL apply in Kanban view, Tabular view, and Closed view. Switching between views while search is active SHALL keep the filter and query unchanged.

#### Scenario: Kanban view filters cards
- **WHEN** search is active with query `foo` and the user is on Kanban view
- **THEN** only TaskCards whose task matches `foo` are visible on the board

#### Scenario: Filter persists across view switch
- **WHEN** search is active with query `bar` and the user switches from Tabular to Kanban
- **THEN** the Kanban view also shows only tasks matching `bar` and the search bar remains visible

### Requirement: Navigation unchanged during search
Arrow keys, `Enter`, `PageUp`, `PageDown`, and `Delete` SHALL work exactly as when no search is active — navigating and acting only on the visible (matching) tasks, as if the hidden tasks do not exist.

#### Scenario: Arrow keys navigate filtered results
- **WHEN** search is active and three tasks match
- **THEN** pressing the down arrow moves focus to the next matching task, not to a hidden one

#### Scenario: Enter opens focused task during search
- **WHEN** search is active and a task is focused
- **THEN** pressing `Enter` opens the task editor

### Requirement: Letter key actions disabled during search
While the search bar is active, single-character key bindings that normally trigger actions (view-switch keys `1`/`2`/`3`, `q`, `r`, `a`, and view-level letter bindings `d`, `n`, `o`) SHALL be captured by the search input and SHALL NOT trigger their bound actions. The characters SHALL be appended to the search query instead.

The `?` key is a **passthrough** — pressing `?` while search is active SHALL open the help overlay as normal but SHALL NOT append `?` to the search query.

The `Backspace` key SHALL edit the search query (remove the last typed character) in all views. `Backspace` SHALL NOT trigger task-deletion in any view; only the `Delete` key retains the delete-task action.

#### Scenario: '1' types into search, not switch view
- **WHEN** search is active and the user presses `1`
- **THEN** `1` is appended to the search query and the view does NOT switch to Kanban

#### Scenario: 'q' types into search, not quit
- **WHEN** search is active and the user presses `q`
- **THEN** `q` is appended to the search query and the app does NOT quit

#### Scenario: '?' opens help without adding to query
- **WHEN** search is active and the user presses `?`
- **THEN** the help overlay opens and `?` is NOT appended to the search query

#### Scenario: Backspace removes last search character
- **WHEN** search is active and the query is `foo` and the user presses `Backspace`
- **THEN** the query becomes `fo` and no task-deletion dialog appears

### Requirement: Search persists through task detail
Opening a task detail form (edit screen) while search is active SHALL keep the search query in memory. When the form is closed, the view SHALL re-render with the same filter still applied.

#### Scenario: Filter restored after closing task form
- **WHEN** search is active with query `foo`, the user opens a task, edits it, and closes the form
- **THEN** the view re-renders showing only tasks matching `foo`
