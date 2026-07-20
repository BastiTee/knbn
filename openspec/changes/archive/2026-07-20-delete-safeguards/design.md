## Context

`action_mark_done` in `kanban.py` calls `_set_status('Done')` directly — no guard, no prompt. The `action_delete_task` method already uses `_ConfirmModal`, so the pattern exists and just needs to be applied to `action_mark_done` as well.

`store.delete_task` removes the CSV row but never touches `~/.knbn/notes/`. The notes path is resolved via `get_notes_path(data_dir, task)` which is already exported and used elsewhere. Deletion of the file is a one-liner after removing the CSV row.

## Goals / Non-Goals

**Goals:**
- Add a confirmation prompt to `action_mark_done` before calling `_set_status('Done')`.
- Delete the notes file (if it exists) in `store.delete_task`.

**Non-Goals:**
- Changing the `Del`/`Backspace` delete confirmation flow (already correct).
- Adding undo/restore functionality.
- Cleaning up pre-existing orphaned notes files.

## Decisions

### Reuse `_ConfirmModal` for Done confirmation

`_ConfirmModal` already exists in `kanban.py` and is used by `action_delete_task`. Reuse it with a softer message (e.g., `Mark "Task title" as Done?`) — no new widget needed.

### Notes deletion in `store.delete_task`

`delete_task(data_dir, index)` already receives `data_dir` and the task list. After removing the CSV row, resolve the notes path with `get_notes_path(data_dir, task)` (using the task *before* deletion) and call `path.unlink(missing_ok=True)`. This is atomic enough for a personal tool — no transaction rollback needed.

## Risks / Trade-offs

- **Done confirmation adds friction**: Every `d` keypress now requires `y`/Enter confirmation. This is intentional — the user reported losing a task unexpectedly. The modal is dismissible with `Esc`/`n` so the cost is low.
- **Notes deletion is irreversible**: Once deleted, notes are gone. Acceptable — this matches the user's expectation that deleting a task cleans up its data.

## Migration Plan

No data migration needed. Orphaned notes files already on disk are unaffected (not cleaned up retroactively).
