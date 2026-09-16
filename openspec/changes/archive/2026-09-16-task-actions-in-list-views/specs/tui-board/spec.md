## MODIFIED Requirements

### Requirement: Tabular view
The TUI SHALL provide a tabular view listing all active tasks grouped by status (`Now`, `Feedback`, `Todo`), sorted within each group by priority descending then `Last edited time` descending. The view SHALL display a non-focusable column-header row at the top with the labels `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due` aligned to the corresponding data columns. Columns SHALL appear in this order: `Name` (28 chars), `Status` (11 chars), `Priority` (9 chars), `Category` (14 chars), `Created` (16 chars), `Edited` (16 chars), `Due`. Date fields SHALL be displayed using `display_date_only()`, showing only `YYYY-MM-DD` regardless of whether a time component is stored. Task rows SHALL be focusable and navigable with `↑`/`↓`. `PgUp`/`PgDn` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task edit form pre-populated with that task's fields. Pressing `d` on a focused row SHALL prompt for confirmation and, on confirmation, transition the task to `BoardConfig.default_terminal_status`, update `date_modified`, persist the change, and reload the view. Pressing `Del` or `Backspace` on a focused row SHALL prompt for confirmation and, on confirmation, permanently delete the task and reload the view.

#### Scenario: Tabular view shows column headers
- **WHEN** the user switches to the Tabular view
- **THEN** a non-focusable header row appears at the top showing `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due`

#### Scenario: Date value shown as date only
- **WHEN** a task has a `date_modified` of `2026-07-21 15:45`
- **THEN** the Edited column shows `2026-07-21` (time component stripped)

#### Scenario: Tabular view groups by status
- **WHEN** the user switches to the Tabular view
- **THEN** tasks are grouped under `Now`, `Feedback`, and `Todo` section headers

#### Scenario: Navigate rows with arrow keys
- **WHEN** the user presses `↑` or `↓` in the Tabular view
- **THEN** focus moves to the previous or next task row and the focused row is visually highlighted

#### Scenario: Skip 10 rows with PgUp
- **WHEN** the user presses `PgUp` on a focused row in the Tabular view
- **THEN** focus moves 10 rows up, clamping at the first row

#### Scenario: Skip 10 rows with PgDn
- **WHEN** the user presses `PgDn` on a focused row in the Tabular view
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

#### Scenario: Mark task done from Tabular view
- **WHEN** the user presses `d` on a focused row in the Tabular view
- **THEN** a confirmation dialog appears; on confirmation the task status changes to `default_terminal_status`, `date_modified` is updated to now, the task disappears from the Tabular view, and focus moves to the next row (or previous if it was the last row)

#### Scenario: Cancel mark-done from Tabular view leaves task unchanged
- **WHEN** the user presses `d` then cancels the confirmation dialog in the Tabular view
- **THEN** the task remains in the Tabular view unchanged

#### Scenario: Delete task from Tabular view
- **WHEN** the user presses `Del` or `Backspace` on a focused row in the Tabular view
- **THEN** a confirmation dialog appears; on confirmation the task is permanently deleted, the view reloads, and focus moves to the next row (or previous if it was the last row)

#### Scenario: Cancel delete from Tabular view leaves task unchanged
- **WHEN** the user presses `Del` or `Backspace` then cancels the confirmation dialog in the Tabular view
- **THEN** the task remains in the Tabular view unchanged

### Requirement: Closed view
The TUI SHALL provide a Closed view (labelled `Closed` in the toolbar, accessible via key `3`) listing tasks whose status is any value in `BoardConfig.terminal_statuses`, grouped by ISO calendar week of `Last edited time`, most recent week first. The view SHALL NOT assume specific status name strings. The view SHALL display a non-focusable column-header row at the top with the labels `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due` aligned to the corresponding data columns. Columns SHALL appear in this order: `Name` (28 chars), `Status` (11 chars), `Priority` (9 chars), `Category` (14 chars), `Created` (16 chars), `Edited` (16 chars), `Due`. Date fields SHALL be displayed using `display_date_only()`, showing only `YYYY-MM-DD` regardless of whether a time component is stored. Week-group headers SHALL use the same background colour as Tabular view group headers (`$primary-darken-2`). Task rows SHALL be focusable and navigable with `↑`/`↓`. `PgUp`/`PgDn` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task edit form pre-populated with that task's fields. Pressing `Del` or `Backspace` on a focused row SHALL prompt for confirmation and, on confirmation, permanently delete the task and reload the view. The `d` key SHALL have no effect in the Closed view — tasks in terminal statuses cannot be marked done again.

#### Scenario: Done view shows all configured terminal statuses
- **WHEN** `terminal_statuses` is `['Done', 'Archived', 'Dropped']`
- **THEN** tasks with any of those three statuses appear in the Done view

#### Scenario: Closed view shows column headers
- **WHEN** the user switches to the Closed view
- **THEN** a non-focusable header row appears at the top showing `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due`

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

#### Scenario: Skip 10 rows with PgUp
- **WHEN** the user presses `PgUp` on a focused row in the Closed view
- **THEN** focus moves 10 rows up, clamping at the first row

#### Scenario: Skip 10 rows with PgDn
- **WHEN** the user presses `PgDn` on a focused row in the Closed view
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

#### Scenario: Delete task from Closed view
- **WHEN** the user presses `Del` or `Backspace` on a focused row in the Closed view
- **THEN** a confirmation dialog appears; on confirmation the task is permanently deleted, the view reloads, and focus moves to the next row (or previous if it was the last row)

#### Scenario: Cancel delete from Closed view leaves task unchanged
- **WHEN** the user presses `Del` or `Backspace` then cancels the confirmation dialog in the Closed view
- **THEN** the task remains in the Closed view unchanged

#### Scenario: d key is no-op in Closed view
- **WHEN** the user presses `d` on a focused row in the Closed view
- **THEN** nothing happens
