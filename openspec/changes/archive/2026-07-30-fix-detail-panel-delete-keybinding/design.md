## Context

The detail panel (`src/knbn/widgets/detail.py`) is opened by pressing `Enter` on any task card. It currently binds `d` to "delete task". The Kanban board binds `Del`/`Backspace` for the same delete action. The inconsistency means users must recall a different key depending on context for the same destructive operation.

## Goals / Non-Goals

**Goals:**
- Make `Del`/`Backspace` trigger delete in the detail panel (matching Kanban board)
- Remove the `d=delete` binding from the detail panel
- Update the help overlay to reflect the corrected keybinding

**Non-Goals:**
- Changing any other keybinding
- Altering delete confirmation behaviour
- Changing Kanban board bindings

## Decisions

**Remove `d` from detail panel, add `Delete`/`Backspace`**

The Kanban board already uses `Del`/`Backspace` for delete (with a confirmation dialog). The detail panel's `d` binding was an independent addition that created the inconsistency. Since `d` is not needed for anything else in the detail panel context, it is simply removed. `delete` and `backspace` are added as the binding keys, matching the board's `BINDINGS` pattern.

No alternative considered — the fix is unambiguous.

## Risks / Trade-offs

- [Muscle memory] Users who already use `d` in the detail panel will need to relearn. → This is intentional: the old binding was the error.
- [No other risk] The change is local to a single widget and one help text entry.
