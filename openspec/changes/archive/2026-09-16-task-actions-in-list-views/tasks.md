## 1. TabularView — mark done action

- [x] 1.1 Add `Binding('d', 'mark_done', 'Done', show=False)` to `TabularView.BINDINGS` in `src/knbn/views/tabular.py` and verify the binding appears in the widget's key handler
- [x] 1.2 Implement `action_mark_done` on `TabularView`: get focused row's `knbn_task` and `task_index`, push `ConfirmDialog(f'Mark "{task.title}" as {terminal}?')`, and on confirmation call `update_task`, reload `self._tasks = load_tasks(self.data_dir)`, then call `self._recompose_keeping_focus()` — verify by manually pressing `d` on a row and confirming it disappears from the view

## 2. TabularView — delete action

- [x] 2.1 Add `Binding('delete', 'delete_task', 'Delete', show=False)` and `Binding('backspace', 'delete_task', 'Delete', show=False)` to `TabularView.BINDINGS` in `src/knbn/views/tabular.py`
- [x] 2.2 Implement `action_delete_task` on `TabularView`: get focused row's `knbn_task` and `task_index`, push `ConfirmDialog(f'Delete "{task.title}"?')`, and on confirmation call `delete_task`, reload `self._tasks`, then call `self._recompose_keeping_focus()` — verify by deleting a task and confirming the row is gone and focus lands on the adjacent row

## 3. ClosedView — delete action

- [x] 3.1 Add `Binding('delete', 'delete_task', 'Delete', show=False)` and `Binding('backspace', 'delete_task', 'Delete', show=False)` to `ClosedView.BINDINGS` in `src/knbn/views/done_week.py`
- [x] 3.2 Implement `action_delete_task` on `ClosedView`: same pattern as `TabularView.action_delete_task` — get focused row, push `ConfirmDialog`, on confirmation call `delete_task`, reload `self._tasks`, call `self._recompose_keeping_focus()` — verify by deleting a closed task and confirming it disappears

## 4. Imports

- [x] 4.1 Add necessary imports to `tabular.py`: `from dataclasses import replace`, `from knbn.model.store import delete_task, load_tasks, update_task`, `from knbn.model.task import now_str`, `from knbn.widgets._confirm import ConfirmDialog` — verify `mypy src/` passes with no new errors
- [x] 4.2 Add necessary imports to `done_week.py`: `from knbn.model.store import delete_task, load_tasks`, `from knbn.widgets._confirm import ConfirmDialog` — verify `mypy src/` passes with no new errors

## 5. Verification

- [x] 5.1 Run `uv run mypy src/` and confirm zero new type errors
- [x] 5.2 Run `uv run pytest tests` and confirm all tests pass
- [x] 5.3 Run `uv run ruff check src/ tests/` and confirm no new lint errors
