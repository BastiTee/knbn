## Why

Navigating between columns on the Kanban board feels unnatural. Pressing `→` from task #2 in `Todo` always lands on task #1 in `Now` (the last-visited row in that column), rather than task #2. Users expect the cursor to stay at the same visual position, matching how spreadsheets, terminal file managers, and most grid-navigation UIs behave. The current independent-row-per-column state breaks that spatial intuition.

## What Changes

- When moving left or right between columns, the target column's focused row is set to the current row index (clamped to the target column's card count).
- The `_focused_row` dict no longer independently remembers a separate position per column across left/right moves — the row is transferred from the source column.
- Up/down navigation within a column is unchanged.
- Corner case: if the source column has 5 tasks and the target only 2, focus lands on the last card (index 1) in the target.

## Capabilities

### New Capabilities

*(none)*

### Modified Capabilities

- `tui-board`: The "Keyboard navigation on board" requirement is updated to specify index-preserving left/right column switching with clamping.

## Impact

- `src/knbn/views/kanban.py` — `action_focus_left` and `action_focus_right` updated to transfer the current row index to the target column before calling `_focus_col_card`
- `openspec/specs/tui-board/spec.md` — updated scenario for left/right navigation
