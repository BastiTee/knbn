## Context

`TabularView` and `DoneByWeekView` both render task rows as plain `Static` widgets, which cannot receive keyboard focus. `KanbanView` achieves navigation by having `TaskCard` (a `Widget` subclass) hold focus and handle `Enter`/other keys. The `TaskDetailPanel` requires a `task_index` (position in the loaded list), the `Task` object, and `data_dir`.

Both list views receive `tasks: list[Task]` today; they do not receive `data_dir`. `app.py` constructs them in `_show_view` without passing `data_dir`.

## Goals / Non-Goals

**Goals:**
- `↑`/`↓` move focus between task rows in TabularView and DoneByWeekView.
- `Enter` on a focused row opens `TaskDetailPanel` for that task.
- Focused row is visually highlighted (distinct background).
- `data_dir` is available inside both views so the detail panel can be pushed.

**Non-Goals:**
- Edit, delete, or other actions directly from list views (those are already available inside the detail panel once it opens).
- Mouse click-to-focus.
- Collapsing/expanding week or status groups.

## Decisions

**Introduce a `TaskRow` focusable widget shared by both views**

Replace the `Static` task-row renders with a small `TaskRow(Widget)` that can receive focus. It renders the same text as today but gains a `focused` pseudo-class background. Both `TabularView` and `DoneByWeekView` yield `TaskRow` instances instead of raw `Static` rows.

Alternative: make the entire view a `ListView` — rejected because the group headers (status / week) would need to be non-selectable items, which complicates the ListView model. A custom widget is simpler.

**View-level `↑`/`↓` bindings, not row-level**

Trapping arrow keys at the view level (in `TabularView`/`DoneByWeekView`) lets us walk a flat list of rows and call `focus()` on the target. This avoids key-event bubbling complexity and mirrors how `KanbanView` controls focus centrally.

**Thread `data_dir` through to list views**

`app.py`'s `_show_view` will pass `data_dir` when constructing `TabularView` and `DoneByWeekView`. Both views store it and supply it to `TaskDetailPanel` on `Enter`.

**`task_index` is the position in the original `self._tasks` list**

Each `TaskRow` stores a reference to its `Task` and its index in the full task list passed to the view. This index is forwarded to `TaskDetailPanel` unchanged, matching the existing Kanban pattern.

## Risks / Trade-offs

- **Done view is read-only by design** — opening `TaskDetailPanel` from it still shows `e`/`d`/`n` bindings. The detail panel's edit/delete actions will work (they call `action_reload` which reloads all tasks), but after reload the done view may show the task in a different position or remove it. This is acceptable behaviour.
- **Index stability**: the index passed to `TaskDetailPanel` is the position in the list at the time the view was last composed. If the user edits a task from the detail panel and `action_reload` fires, the view recomposes with fresh data — indexes reset correctly.
