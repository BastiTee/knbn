## Why

Navigating to an empty lane/column on the Kanban board is impossible: `←`/`→` silently drops focus when the target column has no task cards. Since pressing `a` now pre-populates status and priority from the focused cell, an empty lane is unreachable — the user can't quickly create a task there without manually correcting the form fields.

## What Changes

- Left/right arrow navigation now lands on the first `LaneHeader` in the target column when that column has no task cards, instead of silently doing nothing.
- Up/down navigation inside an empty column remains a no-op (nothing to move between).
- On initial mount, if the first column is empty, focus still falls to the first column's first lane header rather than finding the next non-empty column.
- `get_lane_context()` already handles `LaneHeader` focus, so `a` will correctly pre-populate status and priority from an empty lane.

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `tui-board`: The "Keyboard navigation on board" requirement gains a new scenario: navigating left or right into an empty column focuses that column's first lane header, giving the user a visible focus target and enabling context-aware task creation.

## Impact

- `src/knbn/views/kanban.py` — `_focus_col_card()` falls back to the first `LaneHeader` in the column when no cards exist. No other files change.
