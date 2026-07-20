## Why

Two related bugs make task deletion unsafe and leave orphaned files on disk:

1. Pressing `d` on a focused card **immediately marks it Done** with no confirmation — the user expects `d` to be safe but it silently removes the card from the active board. Only `Del`/`Backspace` (the explicit delete keys) show a confirmation dialog.
2. When a task is permanently deleted (via `Del`/`Backspace`), its associated notes Markdown file under `~/.knbn/notes/` is **not removed**, leaving orphaned `.md` files that accumulate silently.

## What Changes

- `d` on a focused card SHALL prompt for confirmation before marking the task Done (consistent with the existing delete confirmation flow).
- `store.delete_task()` SHALL also delete the task's notes file if it exists.

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `tui-board`: `d` key behavior changes — confirmation required before marking Done.
- `task-store`: `delete_task` must clean up the associated notes file.

## Impact

- `src/knbn/views/kanban.py`: `action_mark_done` — add confirmation modal before calling `_set_status`.
- `src/knbn/model/store.py`: `delete_task` — call `get_notes_path` and unlink the file if it exists.
