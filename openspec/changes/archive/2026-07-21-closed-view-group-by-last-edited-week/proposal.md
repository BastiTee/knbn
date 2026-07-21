## Why

The Closed view groups terminal-status tasks by the ISO calendar week of `Last edited time`, but closing a task (marking Done, Stopped, or Delegated from the Kanban board) does not update `Last edited time`. As a result, tasks appear under their last *form-save* week rather than the week they were actually closed, making the Closed view useless for answering "what did I finish this week?"

## What Changes

- When a task's status changes to a terminal value (`Done`, `Stopped`, `Delegated`) via the Kanban board actions (`d`, `x`, `g`, `Del`), `Last edited time` SHALL be stamped to the current timestamp.
- The Closed view already groups by `Last edited time` — no grouping logic changes are needed.

## Capabilities

### New Capabilities

- none

### Modified Capabilities

- `tui-board`: The requirement for the Closed view already states grouping by `Last edited time`. The requirement for status-change actions (`d`, `x`, `g`, `Del`) must be updated to specify that they stamp `Last edited time` on the task.

## Impact

- `src/knbn/views/kanban.py` — `_set_status()` and `action_delegate()` must include `date_modified=now_str()` in the `replace()` call.
- `openspec/specs/tui-board/spec.md` — update scenarios for Done, Stopped, Delegated, and Delete actions to assert that `Last edited time` is updated.
