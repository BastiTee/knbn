## Why

There is currently no way to delete a task from within the TUI. Users must resort to manually editing the CSV file, which breaks the terminal-native workflow. Adding `d` as a delete shortcut in the task detail panel gives a quick, discoverable path to removal.

## What Changes

- When the task detail panel is open, pressing `d` will prompt for confirmation and then permanently delete the task from the store.
- The board/view will refresh after deletion, with the detail panel dismissed.

## Capabilities

### New Capabilities

*(none)*

### Modified Capabilities

- `tui-board`: The "Task detail panel" requirement gains a new `d` keybinding for task deletion with a confirmation step.

## Impact

- `src/knbn/widgets/detail.py` — new `action_delete_task` and confirmation prompt
- `src/knbn/model/store.py` — new `delete_task(task_id)` function
- `src/knbn/app.py` — handle the post-deletion board refresh
- `openspec/specs/tui-board/spec.md` — updated requirement for detail panel keybindings
