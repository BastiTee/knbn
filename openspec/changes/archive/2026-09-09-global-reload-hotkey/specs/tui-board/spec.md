## MODIFIED Requirements

### Requirement: Global quit
The TUI SHALL quit cleanly when the user presses `q` or `Ctrl+C` from any view.

#### Scenario: Quit with q
- **WHEN** the user presses `q` (not in a text input field)
- **THEN** the TUI exits and the terminal is restored to its prior state

## ADDED Requirements

### Requirement: Global reload
The TUI SHALL reload all tasks from disk when the user presses `r` from any view. The current view SHALL remain active after reload. The reloaded data SHALL reflect any changes made externally (e.g. via `knbn add` in another terminal). No confirmation dialog is required.

#### Scenario: Reload picks up externally added task
- **WHEN** a task is added via `knbn add` in another terminal while the TUI is open
- **AND** the user presses `r`
- **THEN** the newly added task appears in the current view without restarting the TUI

#### Scenario: Reload is available from all views
- **WHEN** the user presses `r` while the Kanban, Tabular, or Closed view is active
- **THEN** the tasks are reloaded from disk and the current view refreshes

#### Scenario: Help overlay lists reload key
- **WHEN** the user opens the help overlay with `?`
- **THEN** `r Reload` appears in the listed key bindings
