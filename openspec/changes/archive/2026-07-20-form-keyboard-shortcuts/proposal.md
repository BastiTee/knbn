## Why

The task add/edit form currently requires reaching for the mouse or tabbing to the Save/Cancel buttons. Power users filling in a task want `Ctrl+S` to save immediately and `Ctrl+C` to cancel — the same muscle memory as editors and other terminal tools. Both shortcuts are missing today.

## What Changes

- `Ctrl+S` in the form saves the task immediately, provided the title field has at least one non-whitespace character
- The existing `Esc` cancel binding is unchanged
- The existing Save/Cancel buttons are unchanged

## Capabilities

### New Capabilities

*(none)*

### Modified Capabilities

- `tui-board`: The "Inline add/edit form" requirement must document the new `Ctrl+S` save shortcut

## Impact

- `src/knbn/widgets/form.py`: Add `ctrl+s` and `ctrl+c` bindings to `TaskForm.BINDINGS`; add `action_save` and `action_ctrl_c` handlers
- No data model, storage, or CLI changes
