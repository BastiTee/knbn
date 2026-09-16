## Context

Both `TabularView` and `ClosedView` extend `RowListView`, a shared base class in `views/_row_list.py`. The base class currently defines BINDINGS for cursor navigation and `enter` for edit. The Kanban view (`views/kanban.py`) already implements `action_mark_done` and `action_delete_task` as methods on the column-based `KanbanView` class and relies on `ConfirmDialog`, `delete_task`, and `update_task` from the model layer. The same model functions are available for use in list views.

`RowListView._recompose_keeping_focus()` already provides a helper that saves the focused row index, recomposes, and refocuses at the saved position (clamped to last row). This is exactly the right behavior for focus restoration after a delete or mark-done: the task at that index is gone, and the next task in its place should receive focus.

## Goals / Non-Goals

**Goals:**
- Add `d` (mark done with confirmation) to `TabularView`
- Add `Del`/`Backspace` (delete with confirmation) to `TabularView` and `ClosedView`
- Restore focus to the next visible row after each action (using the existing `_recompose_keeping_focus` pattern)
- Match Kanban view confirmation dialog text (`Mark "<title>" as <terminal>?` and `Delete "<title>"?`)

**Non-Goals:**
- Adding mark-done to `ClosedView` (tasks already have terminal status)
- Changing the base `RowListView` class bindings (keep changes local to the subclasses to avoid unintended side-effects)
- Modifying the focus-restoration strategy for cursor navigation

## Decisions

**Decision: Add bindings to subclasses, not the base class**

`RowListView` is a shared base for both `TabularView` and `ClosedView`. Adding `d` to the base class would unintentionally expose it in `ClosedView`. Adding `Del`/`Backspace` to the base would be acceptable but would require subclasses to opt out to suppress it. Keeping bindings per-subclass is cleaner and easier to reason about.

Alternatives: a base-class opt-in flag (`allow_mark_done = False`) was considered but adds indirection with no benefit here.

**Decision: Reuse `_recompose_keeping_focus` for focus restoration**

The existing helper saves the focused row index, calls `recompose()` via `call_after_refresh`, then refocuses at `min(saved, last)`. After a delete the task at that index is gone so the next task slides up — producing exactly the right UX. No new mechanism is needed.

**Decision: Access `board_config` via `self._board_config`**

Both `TabularView` and `ClosedView` already define `self._board_config` (a property delegating to `self.app.board_config`). Use this for `default_terminal_status` in mark-done.

**Decision: Reload task list after mutation before recomposing**

Both views store `self._tasks` as a snapshot. After a delete or mark-done, call `load_tasks(self.data_dir)` to update `self._tasks` before recomposing, matching the pattern used in `kanban.py`.

## Risks / Trade-offs

- [Risk] `_recompose_keeping_focus` fires two `call_after_refresh` calls back-to-back; ordering is preserved by the Textual queue, but if Textual's callback ordering changes between versions the refocus could happen before recompose. → Same risk already accepted in `RowListView` for cursor-navigation recompose.
- [Risk] In `ClosedView`, `Del` on a task triggers a full reload of `self._tasks` followed by recompose. Because `ClosedView` only shows terminal-status tasks, the reloaded list and week groupings may shift if another external change happened simultaneously. → Acceptable for a single-user personal tool.
