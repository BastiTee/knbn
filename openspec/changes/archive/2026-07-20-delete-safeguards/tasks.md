## 1. Store: delete notes file on task deletion

- [x] 1.1 In `store.delete_task` (`src/knbn/model/store.py`), capture the task before removing it from the list, then call `get_notes_path(data_dir, task).unlink(missing_ok=True)` after saving the updated CSV

## 2. Kanban: confirm before marking Done

- [x] 2.1 In `action_mark_done` (`src/knbn/views/kanban.py`), wrap the `_set_status('Done')` call in a `_ConfirmModal` prompt (reuse existing modal), only calling `_set_status` in the `on_confirm` callback when `confirmed` is `True`

## 3. Help text

- [x] 3.1 Update `src/knbn/widgets/help.py` — change `d  Mark Done` entry to `d  Mark Done (confirm)` to signal the new confirmation step

## 4. Tests

- [x] 4.1 Add a test in `tests/test_store.py` verifying that `delete_task` deletes the associated notes file when it exists
- [x] 4.2 Add a test verifying that `delete_task` succeeds without error when no notes file exists
