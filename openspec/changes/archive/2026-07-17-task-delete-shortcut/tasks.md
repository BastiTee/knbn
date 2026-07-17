## 1. Confirmation modal

- [x] 1.1 Add a small `DeleteConfirmScreen(ModalScreen[bool])` inline in `detail.py` that shows "Delete task? (y/n)" and returns `True`/`False`

## 2. Detail panel delete action

- [x] 2.1 Add `Binding('d', 'delete_task', 'Delete', show=True)` to `TaskDetailPanel.BINDINGS`
- [x] 2.2 Implement `action_delete_task` in `TaskDetailPanel`: push `DeleteConfirmScreen`, resolve task index by matching `task_id` in loaded tasks, call `store.delete_task`, dismiss the panel, and trigger a board recompose

## 3. Help overlay update

- [x] 3.1 Add `d Delete` entry to the help overlay keybinding list in `widgets/help.py`

## 4. Tests

- [x] 4.1 Add unit test for `delete_task` store function (task is removed, remaining tasks are intact) — check if already covered in `test_store.py`
- [x] 4.2 Verify full build passes: `make build`
