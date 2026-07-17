## MODIFIED Requirements

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

### Requirement: Done-by-week view
The TUI SHALL provide a Done-by-week view listing terminal-status tasks (`Done`, `Delegated`, `Stopped`) grouped by ISO calendar week of `Last edited time`, most recent week first. Columns: `Name`, `Category`, `Priority`, `Last edited time`, `Date Created`. Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task detail panel.

#### Scenario: Done tasks grouped by week
- **WHEN** the user switches to the Done-by-week view
- **THEN** tasks appear under week-range headers (e.g. `Jul 12–18 2026  7`)

#### Scenario: Navigate rows with arrow keys
- **WHEN** the user presses `↑` or `↓` in the Done-by-week view
- **THEN** focus moves to the previous or next task row and the focused row is visually highlighted

#### Scenario: Skip 10 rows with Shift+Up
- **WHEN** the user presses `Shift+↑` on a focused row in the Done-by-week view
- **THEN** focus moves 10 rows up, clamping at the first row

#### Scenario: Skip 10 rows with Shift+Down
- **WHEN** the user presses `Shift+↓` on a focused row in the Done-by-week view
- **THEN** focus moves 10 rows down, clamping at the last row

#### Scenario: Tab does nothing in Done view
- **WHEN** the user presses Tab or Shift+Tab in the Done-by-week view
- **THEN** focus does not change

#### Scenario: Auto-focus first row on mount
- **WHEN** the Done-by-week view is displayed
- **THEN** the first task row is immediately focused without any keypress

#### Scenario: Open detail panel from done view
- **WHEN** the user presses `Enter` on a focused task row in the Done-by-week view
- **THEN** the task detail panel opens for that task

### Requirement: Keyboard navigation on board
The TUI SHALL support arrow key navigation between cards on the Kanban board, `Enter` to open the task detail panel, `e` to edit, `d` to mark done, `x` to stop, `g` to delegate, `m` to move to a different status, `p` to change priority, and `Del`/`Backspace` with confirmation to delete a task. Tab and Shift+Tab SHALL have no effect in the Kanban view. The first card in the top-left occupied cell SHALL receive focus automatically when the Kanban view is mounted. When moving left or right between columns, focus SHALL land on the card at the same row index as the current card (counting from the top of the column, ignoring swimlane boundaries), clamped to the last card if the target column has fewer cards. `Shift+↑`/`Shift+↓` SHALL change the focused card's priority one step up or down (`High ↔ Medium ↔ Low`), clamping at the boundaries; after the move the card SHALL remain focused in its new swim lane. `Shift+←`/`Shift+→` SHALL move the focused card to the adjacent active status column (`Todo ↔ Now ↔ Feedback`), clamping at the boundaries; after the move the card SHALL remain focused in its new column. Terminal statuses (`Done`, `Delegated`, `Stopped`) are not reachable via Shift+arrow gestures.

#### Scenario: Arrow navigation between cards
- **WHEN** the user presses `←`/`→` on the board
- **THEN** focus moves between columns

#### Scenario: Index-preserving column switch
- **WHEN** the user is focused on the 2nd card in `Todo` and presses `←` or `→`
- **THEN** focus moves to the 2nd card in the adjacent column (counting from the top regardless of swimlane)

#### Scenario: Clamped column switch
- **WHEN** the user is focused on the 5th card in `Todo` and presses `←` to `Now` which only has 2 cards
- **THEN** focus moves to the last card (2nd) in `Now`

#### Scenario: Mark task done
- **WHEN** the user presses `d` on a focused card
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
