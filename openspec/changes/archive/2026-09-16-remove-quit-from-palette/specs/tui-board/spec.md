## MODIFIED Requirements

### Requirement: Command palette
The TUI SHALL expose a command palette via `Ctrl+P`. The palette SHALL contain exactly the following commands in order: `Theme`, `Keys`. The `Quit`, `Screenshot`, and `Maximize`/`Minimize` commands SHALL NOT appear in the palette. The application SHALL NOT display a title header bar; no mouse-clickable palette trigger SHALL be present.

#### Scenario: Palette shows Theme then Quit
- **WHEN** the user opens the command palette with `Ctrl+P`
- **THEN** the only entries listed are `Theme` and `Keys`, in that order, and no `Quit` entry appears

#### Scenario: Screenshot absent from palette
- **WHEN** the user opens the command palette
- **THEN** no `Screenshot` command is listed

#### Scenario: Maximize absent from palette
- **WHEN** the user opens the command palette
- **THEN** no `Maximize` or `Minimize` command is listed

#### Scenario: No title header bar rendered
- **WHEN** the TUI is launched
- **THEN** no header bar is displayed at the top of the screen
