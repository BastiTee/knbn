## Why

When tasks are added via `knbn add` in another terminal tab, the TUI has no way to pick up those changes without quitting and restarting. A global reload hotkey lets users refresh the in-memory task list from disk without leaving the board.

## What Changes

- Add a global `r` keybinding available in all three views (Kanban, Tabular, Closed)
- Pressing `r` re-reads `tasks.csv` from disk and redraws the current view
- The current view and focus position are preserved where possible

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `tui-board`: Add the `r` reload keybinding requirement and remove the "There is no dedicated Reload keybinding" statement

## Impact

- `src/knbn/app.py`: new `action_reload` method + BINDINGS entry
- `openspec/specs/tui-board/spec.md`: update keybindings section and remove the explicit negation
