# active-tab-indicator

## Purpose

TBD

## Requirements

### Requirement: Active tab indicator in footer
The footer toolbar SHALL visually distinguish the currently active view tab key (`1`, `2`, or `3`) from the inactive ones. The active key SHALL be rendered with bold text style so it is immediately recognisable without relying on colour alone. The indicator SHALL update immediately whenever the active view changes.

#### Scenario: Active tab key is bold on Kanban view
- **WHEN** the Kanban view is active
- **THEN** the `1` key label in the footer is rendered in bold and the `2` and `3` key labels are not bold

#### Scenario: Active tab key updates on view switch
- **WHEN** the user presses `2` to switch to the Tabular view
- **THEN** the `2` key label in the footer becomes bold and the `1` key label returns to normal weight

#### Scenario: Active tab key is bold on Closed view
- **WHEN** the Closed view is active
- **THEN** the `3` key label in the footer is rendered in bold and the `1` and `2` key labels are not bold
