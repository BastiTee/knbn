## 1. Extend TaskForm with initial status/priority params

- [x] 1.1 Add `initial_status: str | None = None` and `initial_priority: str | None = None` params to `TaskForm.__init__` and store them as instance attributes
- [x] 1.2 In `TaskForm.compose()`, use `initial_status` / `initial_priority` as the `Select` default value when `existing_task is None` (fall back to `'Todo'` / `'Medium'` if `None`)

## 2. Add lane context detection to KanbanView

- [x] 2.1 Add `get_lane_context() -> tuple[str, str] | None` method to `KanbanView`

## 3. Wire context into app.py

- [x] 3.1 In `KnbnApp.action_add_task`, query for `KanbanView` when `_current_view == 'kanban'`, call `get_lane_context()`, and pass the result as `initial_status` / `initial_priority` to `TaskForm`
