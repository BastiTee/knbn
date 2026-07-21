## MODIFIED Requirements

### Requirement: Tabular view
The TUI SHALL provide a tabular view listing all active tasks grouped by status (`Now`, `Feedback`, `Todo`), sorted within each group by priority descending then `Last edited time` descending. The view SHALL display a non-focusable column-header row at the top with the labels `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date` aligned to the corresponding data columns. Columns SHALL appear in this order: `Name` (28 chars), `Status` (11 chars), `Priority` (9 chars), `Category` (14 chars), `Created` (16 chars), `Edited` (16 chars), `Due Date`. Date fields SHALL be displayed using `display_date()`: showing `YYYY-MM-DD HH:MM` when a time component is present in the stored value, or `YYYY-MM-DD` when only a date is stored. Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task detail panel.

#### Scenario: Tabular view shows column headers
- **WHEN** the user switches to the Tabular view
- **THEN** a non-focusable header row appears at the top showing `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date`

#### Scenario: Tabular view groups by status
- **WHEN** the user switches to the Tabular view
- **THEN** tasks are grouped under `Now`, `Feedback`, and `Todo` section headers

#### Scenario: Date-only value shown without time
- **WHEN** a task has a `date_modified` of `2026-07-21` (no time component)
- **THEN** the Edited column shows `2026-07-21`

#### Scenario: Datetime value shown with time
- **WHEN** a task has a `date_modified` of `2026-07-21 15:45`
- **THEN** the Edited column shows `2026-07-21 15:45`

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

### Requirement: Closed view
The TUI SHALL provide a Closed view (labelled `Closed` in the toolbar, accessible via key `3`) listing terminal-status tasks (`Done`, `Delegated`, `Stopped`) grouped by ISO calendar week of `Last edited time`, most recent week first. The view SHALL display a non-focusable column-header row at the top with the labels `Name`, `Status`, `Priority`, `Category`, `Created`, `Edited`, `Due Date` aligned to the corresponding data columns. Columns SHALL appear in this order: `Name` (28 chars), `Status` (11 chars), `Priority` (9 chars), `Category` (14 chars), `Created` (16 chars), `Edited` (16 chars), `Due Date`. Date fields SHALL be displayed using `display_date()`: showing `YYYY-MM-DD HH:MM` when a time component is present, or `YYYY-MM-DD` when only a date is stored. Week-group headers SHALL use the same background colour as Tabular view group headers (`$primary-darken-2`). Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task detail panel.

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

#### Scenario: Open detail panel from closed view
- **WHEN** the user presses `Enter` on a focused task row in the Closed view
- **THEN** the task detail panel opens for that task

### Requirement: Inline add/edit form
The TUI SHALL provide an overlay form for creating and editing tasks, accessible via `a` (add) from any view and `e` from a focused card or detail panel. The form SHALL be dismissible with `Esc`. The form SHALL be saveable with `Ctrl+S` provided the title field contains at least one non-whitespace character. The Due field label SHALL read `Due (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional)`. When saving, if the Due field is non-empty and does not match `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`, the form SHALL display an inline validation error below the Due field and SHALL NOT save the task.

#### Scenario: Open add form
- **WHEN** the user presses `a`
- **THEN** an overlay form appears with empty fields ready for input

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
