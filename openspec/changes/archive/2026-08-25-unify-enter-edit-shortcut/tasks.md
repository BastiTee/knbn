## 1. Remove detail panel widget

- [x] 1.1 Delete `src/knbn/widgets/detail.py`
- [x] 1.2 Remove all imports of `TaskDetailPanel` / `detail` from `app.py`, `kanban.py`, and any other file that references it
- [x] 1.3 Remove the `on_task_detail_panel_*` and detail-panel-related message handlers from `app.py`

## 2. Wire Enter → edit form in Kanban view

- [x] 2.1 In `src/knbn/views/kanban.py`, remove the `Enter` binding that opens `TaskDetailPanel`
- [x] 2.2 In `src/knbn/views/kanban.py`, remove the `e` binding that opens `TaskForm`
- [x] 2.3 In `src/knbn/views/kanban.py`, add a single `Enter` binding that opens `TaskForm` pre-populated with the focused card's task

## 3. Wire Enter → edit form in Tabular and Closed views

- [x] 3.1 In `src/knbn/views/_row_list.py` (or `tabular.py`), change the `Enter` handler from opening `TaskDetailPanel` to opening `TaskForm` pre-populated with the focused row's task
- [x] 3.2 In `src/knbn/views/done_week.py`, change the `Enter` handler from opening `TaskDetailPanel` to opening `TaskForm` pre-populated with the focused row's task
- [x] 3.3 Remove any `e` binding in `_row_list.py`, `tabular.py`, or `done_week.py`

## 4. Update help overlay

- [x] 4.1 In `src/knbn/widgets/help.py`, remove the `e – Edit task` and `Enter – Open task detail` entries
- [x] 4.2 In `src/knbn/widgets/help.py`, add a single `Enter – Edit task` entry in the appropriate section (consistent across all views)

## 5. Verify and clean up

- [x] 5.1 Run `uv run mypy src/` and resolve any type errors from the removed widget
- [x] 5.2 Run `uv run ruff check src/ tests/` and fix any lint issues
- [x] 5.3 Run `uv run pytest tests/` and confirm the full test suite passes
- [ ] 5.4 Manually launch `uv run knbn board` and verify `Enter` opens the edit form in all three views (Kanban, Tabular, Closed) and that `e` no longer does anything
