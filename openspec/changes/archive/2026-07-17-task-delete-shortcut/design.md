## Context

`knbn` tasks are stored in `tasks.csv`. The store module already has a `delete_task(data_dir, index)` function that removes a task by its list index. The TUI's `TaskDetailPanel` is a `ModalScreen` with keybindings for `Esc`/`q`, `e`, `n`, and `o`. There is currently no way to delete a task without leaving the TUI.

## Goals / Non-Goals

**Goals:**
- Add `d` keybinding in `TaskDetailPanel` that deletes the current task after a confirmation prompt.
- Refresh the active view after deletion and dismiss the detail panel.

**Non-Goals:**
- Soft-delete / archiving (that's the existing `Status: Done` workflow).
- Undo / recovery of deleted tasks.
- Delete shortcut anywhere other than the detail panel.

## Decisions

**Confirmation via `app.push_screen` with a simple Yes/No modal**
The delete action is irreversible, so a one-key confirmation is required. The lightest approach is a small inline `ModalScreen` that presents "Delete this task? (y/n)" and resolves to a bool. This keeps the confirmation self-contained in `detail.py` with no new widget file needed.

Alternative considered: a `notify`/toast with a timed undo — rejected because `knbn` is file-backed with no in-memory undo stack; adding one would be disproportionate for a v1 feature.

**Index resolution at delete time**
`delete_task` takes a list index. The detail panel holds a `knbn_task` reference but not its index. The index must be resolved by finding the task in the current loaded list at delete time (match by `task_id`). This is safe because the detail panel is modal and no concurrent edits can occur while it is open.

**Board refresh via `app.call_after_refresh`**
After deletion the panel is dismissed and the parent view needs a `recompose()`. Posting a message or calling `app.call_after_refresh` from the dismiss callback is the idiomatic Textual pattern already used in the edit flow.

## Risks / Trade-offs

- **Accidental delete**: Mitigated by the confirmation prompt. The keybinding `d` is not used by any other binding in the panel, minimising mis-fires.
- **Index drift**: If the task list were mutated between panel open and confirmation (e.g., by a background process editing the CSV), the wrong task could be deleted. This risk is accepted — `knbn` is a single-user local tool and no background writer exists.
