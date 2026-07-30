## Why

The detail panel currently binds `d` to delete a task, while the Kanban board uses `Del`/`Backspace` for the same action. This inconsistency forces users to remember two different keybindings for the same destructive operation depending on where they are.

## What Changes

- Remove `d=delete` from the detail panel keybinding and help text
- Add `Del`/`Backspace` as the delete trigger in the detail panel (matching Kanban board behaviour)
- `d` in the detail panel remains free (currently it shadows the board-level `d=done` which is already inaccessible from inside the panel — removing it is a safe cleanup)

## Capabilities

### New Capabilities

_(none — this is a behaviour correction, not a new capability)_

### Modified Capabilities

- `tui-board`: The "Task detail panel" requirement currently specifies `d` to delete; it must be updated to specify `Del`/`Backspace` instead.

## Impact

- `src/knbn/widgets/detail.py` — keybinding declaration and handler
- `src/knbn/widgets/help.py` — help overlay key listing for the detail panel
- `openspec/specs/tui-board/spec.md` — "Task detail panel" requirement updated
