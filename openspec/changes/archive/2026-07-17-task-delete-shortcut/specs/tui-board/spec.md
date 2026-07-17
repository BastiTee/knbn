## MODIFIED Requirements

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
