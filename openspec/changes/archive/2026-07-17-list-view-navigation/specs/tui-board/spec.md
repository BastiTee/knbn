## MODIFIED Requirements

### Requirement: Tabular view
The TUI SHALL provide a tabular view listing all active tasks grouped by status (`Now`, `Feedback`, `Todo`), sorted within each group by priority descending then `Last edited time` descending. Columns: `Name`, `Priority`, `Category`, `Due`. Task rows SHALL be focusable and navigable with `↑`/`↓`. Pressing `Enter` on a focused row SHALL open the task detail panel.

#### Scenario: Tabular view groups by status
- **WHEN** the user switches to the Tabular view
- **THEN** tasks are grouped under `Now`, `Feedback`, and `Todo` section headers

#### Scenario: Navigate rows with arrow keys
- **WHEN** the user presses `↑` or `↓` in the Tabular view
- **THEN** focus moves to the previous or next task row and the focused row is visually highlighted

#### Scenario: Open detail panel from tabular view
- **WHEN** the user presses `Enter` on a focused task row in the Tabular view
- **THEN** the task detail panel opens for that task

### Requirement: Done-by-week view
The TUI SHALL provide a Done-by-week view listing terminal-status tasks (`Done`, `Delegated`, `Stopped`) grouped by ISO calendar week of `Last edited time`, most recent week first. Columns: `Name`, `Category`, `Priority`, `Last edited time`, `Date Created`. Task rows SHALL be focusable and navigable with `↑`/`↓`. Pressing `Enter` on a focused row SHALL open the task detail panel.

#### Scenario: Done tasks grouped by week
- **WHEN** the user switches to the Done-by-week view
- **THEN** tasks appear under week-range headers (e.g. `Jul 12–18 2026  7`)

#### Scenario: Navigate rows with arrow keys
- **WHEN** the user presses `↑` or `↓` in the Done-by-week view
- **THEN** focus moves to the previous or next task row and the focused row is visually highlighted

#### Scenario: Open detail panel from done view
- **WHEN** the user presses `Enter` on a focused task row in the Done-by-week view
- **THEN** the task detail panel opens for that task
