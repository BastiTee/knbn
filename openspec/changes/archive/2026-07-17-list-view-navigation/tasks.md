## 1. Shared TaskRow widget

- [x] 1.1 Create `src/knbn/views/_row.py` with a `TaskRow(Widget)` class that accepts `task_index: int`, `knbn_task: Task`, `row_text: str`; renders the text as a `Static`; and has a focused-state CSS highlight

## 2. Tabular view

- [x] 2.1 Add `data_dir: Path` parameter to `TabularView.__init__` and store it
- [x] 2.2 Replace `Static(row, classes='task-row')` yields with `TaskRow(idx, task, row)` yields, passing the task's index in the full task list
- [x] 2.3 Add `BINDINGS` with `↑`/`↓` and `enter` to `TabularView`; implement `action_cursor_up`, `action_cursor_down`, `action_open_detail` that walk the flat row list and push `TaskDetailPanel`

## 3. Done-by-week view

- [x] 3.1 Add `data_dir: Path` parameter to `DoneByWeekView.__init__` and store it
- [x] 3.2 Replace `Static(row, classes='done-row')` yields with `TaskRow(idx, task, row)` yields, passing the task's global index (position in the original `tasks` list)
- [x] 3.3 Add `BINDINGS` with `↑`/`↓` and `enter` to `DoneByWeekView`; implement the same cursor actions

## 4. Wire up data_dir in app.py

- [x] 4.1 Pass `data_dir=self.data_dir` when constructing `TabularView` and `DoneByWeekView` in `app.py`'s `_show_view`

## 5. Help overlay

- [x] 5.1 Add a "List views" section to `widgets/help.py` documenting `↑`/`↓` and `Enter` for Tabular and Done views

## 6. Verify

- [x] 6.1 Run `make build` and confirm all tests pass and type-checking is clean
