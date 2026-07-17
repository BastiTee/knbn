## 1. Bindings and actions in KanbanView

- [x] 1.1 Add four bindings to `KanbanView.BINDINGS`: `shift+up`, `shift+down`, `shift+left`, `shift+right`
- [x] 1.2 Implement `action_move_up`: promote priority one step (clamp at `High`), call `update_task`, reload board, refocus
- [x] 1.3 Implement `action_move_down`: demote priority one step (clamp at `Low`), call `update_task`, reload board, refocus
- [x] 1.4 Implement `action_move_left`: move to previous status in `_STATUS_ORDER` (clamp at index 0), call `update_task`, reload board, refocus
- [x] 1.5 Implement `action_move_right`: move to next status in `_STATUS_ORDER` (clamp at last index), call `update_task`, reload board, refocus

## 2. Help overlay

- [x] 2.1 Add `Shift+↑↓` (priority) and `Shift+←→` (move lane) entries to the Kanban board section in `widgets/help.py`

## 3. Verify

- [x] 3.1 Run `make build` and confirm all tests pass and type-checking is clean
