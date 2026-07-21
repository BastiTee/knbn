## Context

The Closed view groups terminal-status tasks by the ISO calendar week of `Last edited time` (`date_modified`). However, the Kanban board actions that close a task — `d` (Done), `x` (Stopped), `g` (Delegate), and `Del`/`Backspace` (Delete) — use `dataclasses.replace(task, status=new_status)` without updating `date_modified`. The field is only updated when a task is saved through the edit form (`widgets/form.py`). As a result, a task closed this week still shows under the week it was last edited in the form.

## Goals / Non-Goals

**Goals:**
- Stamp `date_modified` to the current time whenever a status-change action transitions a task to a terminal status from the Kanban board.

**Non-Goals:**
- Changing how the Closed view groups or renders tasks — it already groups by `date_modified` correctly.
- Stamping `date_modified` for non-terminal status moves (e.g. `Todo → Now`), which are already handled when needed through form saves.
- Modifying the edit form path — it already stamps `date_modified` on save.

## Decisions

### Stamp `date_modified` inside `_set_status` and `action_delegate`

`kanban.py` has two code paths that transition tasks to terminal statuses:

1. `_set_status(new_status)` — used by `action_mark_done` (→ `Done`) and `action_mark_stopped` (→ `Stopped`).
2. `action_delegate()` — used by `g` (→ `Delegated`).

The fix is to add `date_modified=now_str()` to the `replace()` call in each path. `now_str()` is already imported from `knbn.model.task` in the form widget; it needs to be added to kanban's import.

Delete (`action_delete_task`) removes the task entirely — no `date_modified` stamp needed.

**Alternative considered:** Stamp inside `store.update_task()` automatically. Rejected — `update_task` is a general-purpose writer used by form saves that already carry the correct timestamp; auto-stamping there would double-write and violate single-responsibility.

## Risks / Trade-offs

- [Risk] Existing tasks already in terminal status have stale `date_modified` values → No mitigation needed; the fix applies to future closures only. Existing data is unaffected.
- [Trade-off] `_set_status` is used only for Done/Stopped today; if it is ever reused for non-terminal transitions the stamp would be incorrect → Acceptable: the function name signals finality and callers control which statuses are passed.
