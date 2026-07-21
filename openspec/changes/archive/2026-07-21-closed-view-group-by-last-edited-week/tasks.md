## 1. Implementation

- [x] 1.1 Add `now_str` to the imports from `knbn.model.task` in `src/knbn/views/kanban.py`
- [x] 1.2 In `_set_status()`, add `date_modified=now_str()` to the `replace()` call so Done and Stopped actions stamp the close timestamp
- [x] 1.3 In `action_delegate()`, add `date_modified=now_str()` to the `replace()` call so the Delegated action stamps the close timestamp

## 2. Verification

- [x] 2.1 Mark a task Done from the Kanban board and open the Closed view — confirm it appears under the current ISO week header
- [x] 2.2 Mark a task Stopped from the Kanban board — confirm same grouping behaviour
- [x] 2.3 Delegate a task from the Kanban board — confirm same grouping behaviour
- [x] 2.4 Run `uv run pytest tests` and confirm all tests pass
- [x] 2.5 Run `uv run mypy src/` and confirm no type errors
