## Why

After a board-mutating action (lane collapse/expand, task deletion, mark-done), the Kanban view calls `recompose()` which tears down and recreates all widgets. Because the previously-focused widget no longer exists after recompose, Textual leaves focus in an undefined state and the user must press Tab before keyboard navigation works again.

## What Changes

- After toggling a lane collapsed/expanded, the `LaneHeader` that was toggled SHALL remain focused.
- After a task is deleted from the board, focus SHALL land on the nearest remaining focusable element in the same column (next card down, else next card up, else first lane header in the column, else fall back to column 0).
- After a task is marked done from the board, focus SHALL land on the nearest remaining focusable element using the same rule as deletion.

## Capabilities

### New Capabilities

*(none — this change fixes existing behaviour; no new user-visible capabilities are introduced)*

### Modified Capabilities

- `tui-board`: Requirements and scenarios for post-action focus restoration in the Kanban view need to be added. Specifically: swim-lane toggle focus retention, and focus landing rules after delete and mark-done.

## Impact

- `src/knbn/views/kanban.py` — `on_lane_header_toggled`, `_set_status`, and `action_delete_task` need refocus logic added after recompose.
- `openspec/specs/tui-board/spec.md` — new scenarios under *Keyboard navigation on board* requirement.
