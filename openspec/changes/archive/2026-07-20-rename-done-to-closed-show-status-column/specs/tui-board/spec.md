## MODIFIED Requirements

### Requirement: View switching
The TUI SHALL allow switching between views via keyboard: `1` for Kanban, `2` for Tabular, `3` for Closed. The footer toolbar SHALL display the `q Quit` button to the left of the three view-switching buttons (`1 Kanban`, `2 Tabular`, `3 Closed`).

#### Scenario: Switch to tabular view
- **WHEN** the user presses `2`
- **THEN** the Tabular view replaces the Kanban board

#### Scenario: Switch to closed view
- **WHEN** the user presses `3`
- **THEN** the Closed view replaces the current view

#### Scenario: Quit button appears left of view buttons
- **WHEN** the footer toolbar is rendered
- **THEN** the `q` button appears to the left of the `1`, `2`, and `3` view-switching buttons

### Requirement: Closed view
The TUI SHALL provide a Closed view (labelled `Closed` in the toolbar, accessible via key `3`) listing terminal-status tasks (`Done`, `Delegated`, `Stopped`) grouped by ISO calendar week of `Last edited time`, most recent week first. Columns: `Name`, `Status`, `Category`, `Priority`, `Last edited time`, `Date Created`. Each row SHALL display the task's status value (`Done`, `Delegated`, or `Stopped`). Task rows SHALL be focusable and navigable with `↑`/`↓`. `Shift+↑`/`Shift+↓` SHALL move focus 10 rows at a time, clamping at the first and last row. Tab and Shift+Tab SHALL have no effect in this view. The first row SHALL receive focus automatically when the view is mounted. Pressing `Enter` on a focused row SHALL open the task detail panel.

#### Scenario: Closed tasks grouped by week
- **WHEN** the user switches to the Closed view
- **THEN** tasks appear under week-range headers (e.g. `Jul 12–18 2026  7`)

#### Scenario: Row shows task status
- **WHEN** a Delegated task appears in the Closed view
- **THEN** the row displays `Delegated` in the Status column

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
