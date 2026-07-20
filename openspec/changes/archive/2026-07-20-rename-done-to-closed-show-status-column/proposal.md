## Why

The "Done" view (key `3`) already queries all three terminal statuses (`Done`, `Delegated`, `Stopped`) but the row text does not show which status a task has, making it impossible to distinguish closed tasks at a glance. The tab label "Done" is also misleading — delegated and stopped tasks are not done. Renaming to "Closed" and adding a status column makes the view accurate and informative.

## What Changes

- Rename every reference to the "Done" view/tab to "Closed": binding label, action name, view class, module docstring, help overlay, archive-bar label in the kanban view, and the canonical spec.
- Add a `Status` column to each row in the Closed view, showing `Done`, `Delegated`, or `Stopped`.
- Adjust column layout in `row_text` to fit the new field without wrapping.

## Capabilities

### New Capabilities

<!-- None -->

### Modified Capabilities

- `tui-board`: Rename "Done view" → "Closed view"; add Status column to row display.

## Impact

- `src/knbn/views/done_week.py`: rename class `DoneByWeekView` → `ClosedView`, update docstring, update `row_text` to include `task.status`.
- `src/knbn/app.py`: rename binding label `'Done'` → `'Closed'`, action `action_show_done_week` → `action_show_closed`, internal view key `'done_week'` → `'closed'`, import alias.
- `src/knbn/widgets/help.py`: update `3  Done-by-week view` line to `3  Closed view`.
- `src/knbn/views/kanban.py`: update `#archive-bar` static text header labels (no functional change).
- `openspec/specs/tui-board/spec.md`: rename "Done view" requirement and all references.
