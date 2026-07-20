## MODIFIED Requirements

### Requirement: Global quit
The TUI SHALL quit cleanly when the user presses `q` or `Ctrl+C` from any view. There is no dedicated Reload keybinding.

#### Scenario: Quit with q
- **WHEN** the user presses `q` (not in a text input field)
- **THEN** the TUI exits and the terminal is restored to its prior state

### Requirement: Command palette
The TUI SHALL expose a command palette via `Ctrl+P`. The palette SHALL contain exactly the following commands in order: `Theme`, `Quit`, `Keys`. The `Screenshot` and `Maximize`/`Minimize` commands SHALL NOT appear in the palette.

#### Scenario: Palette shows Theme then Quit
- **WHEN** the user opens the command palette with `Ctrl+P`
- **THEN** the first entry is `Theme` and the second entry is `Quit`

#### Scenario: Screenshot absent from palette
- **WHEN** the user opens the command palette
- **THEN** no `Screenshot` command is listed

#### Scenario: Maximize absent from palette
- **WHEN** the user opens the command palette
- **THEN** no `Maximize` or `Minimize` command is listed
