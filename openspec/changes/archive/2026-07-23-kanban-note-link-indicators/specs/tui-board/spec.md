## MODIFIED Requirements

### Requirement: Keyboard navigation on board
The TUI SHALL support arrow key navigation between cards on the Kanban board, `Enter` to open the task detail panel, `e` to edit, `d` to mark Done (with confirmation), `x` to stop, `g` to delegate, `m` to move to a different status, `p` to change priority, `o` to open the focused card's `key_resource` URL in the default browser (no-op if no URL is set), and `Del`/`Backspace` with confirmation to delete a task. Tab and Shift+Tab SHALL have no effect in the Kanban view. The first card in the top-left occupied cell SHALL receive focus automatically when the Kanban view is mounted. When moving left or right between columns, focus SHALL land on the card at the same row index as the current card (counting from the top of the column, ignoring swimlane boundaries), clamped to the last card if the target column has fewer cards. `PgUp`/`PgDn` SHALL reorder the focused card within its lane or move it to the adjacent priority lane. `Shift+←`/`Shift+→` SHALL move the focused card to the adjacent active status column (`Todo ↔ Now ↔ Feedback`), clamping at the boundaries; after the move the card SHALL remain focused in its new column. Terminal statuses (`Done`, `Delegated`, `Stopped`) are not reachable via Shift+arrow gestures. Marking a task Done, Stopped, or Delegated SHALL update `Last edited time` to the current timestamp at the moment of confirmation.

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
