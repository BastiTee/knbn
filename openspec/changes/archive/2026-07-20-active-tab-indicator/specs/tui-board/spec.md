## MODIFIED Requirements

### Requirement: View switching
The TUI SHALL allow switching between views via keyboard: `1` for Kanban, `2` for Tabular, `3` for Closed. The footer toolbar SHALL display the `q Quit` button to the left of the three view-switching buttons (`1 Kanban`, `2 Tabular`, `3 Closed`). The footer SHALL visually indicate which view is currently active by rendering the corresponding tab key in bold.

#### Scenario: Switch to tabular view
- **WHEN** the user presses `2`
- **THEN** the Tabular view replaces the Kanban board

#### Scenario: Switch to closed view
- **WHEN** the user presses `3`
- **THEN** the Closed view replaces the current view

#### Scenario: Quit button appears left of view buttons
- **WHEN** the footer toolbar is rendered
- **THEN** the `q` button appears to the left of the `1`, `2`, and `3` view-switching buttons

#### Scenario: Active tab key is highlighted in footer
- **WHEN** a view is active
- **THEN** the corresponding tab key (`1`, `2`, or `3`) in the footer is rendered in bold to indicate the active view
