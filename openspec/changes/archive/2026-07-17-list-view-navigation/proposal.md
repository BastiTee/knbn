## Why

The Tabular and Done-by-week views are currently read-only displays — the user cannot move focus between rows or open a task from either view. This makes them second-class citizens compared to the Kanban board, where every task is focusable and actionable. Users navigating to these views to inspect or edit a task have no way to do so without switching back to the board.

## What Changes

- Both `TabularView` and `DoneByWeekView` will support `↑`/`↓` keyboard navigation between task rows.
- Pressing `Enter` on a focused row will open the `TaskDetailPanel` for that task (same panel used on the Kanban board).
- The currently focused row will be visually highlighted so the user always knows which task is selected.

## Capabilities

### New Capabilities

*(none)*

### Modified Capabilities

- `tui-board`: The "Tabular view" and "Done-by-week view" requirements gain row navigation and `Enter`-to-detail behaviour.

## Impact

- `src/knbn/views/tabular.py` — rows converted from `Static` to a focusable widget; view gains `↑`/`↓` bindings and an `Enter` handler
- `src/knbn/views/done_week.py` — same treatment
- `src/knbn/widgets/help.py` — new section or updated section documenting the new bindings for list views
- `src/knbn/app.py` — `data_dir` must be threaded through to the list views so the detail panel can be pushed
- `openspec/specs/tui-board/spec.md` — updated requirements for Tabular and Done-by-week views
