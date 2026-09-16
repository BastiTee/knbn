## Why

The Tabular (view 2) and Closed (view 3) list views currently only support task editing via `Enter`, leaving users unable to delete tasks or mark them done without switching to the Kanban board. This creates unnecessary friction for common task housekeeping operations.

## What Changes

- **Tabular view (view 2)**: Add `d` to mark the focused task done (with confirmation) and `Del`/`Backspace` to delete the focused task (with confirmation).
- **Closed view (view 3)**: Add `Del`/`Backspace` to delete the focused task (with confirmation). Mark-done is NOT available here — tasks are already in a terminal status.
- After delete or mark-done, focus SHALL be restored to a well-defined row (next row below, or row above if last, or first row if view is empty).
- Keyboard shortcuts are identical to those already defined for the Kanban view.

## Capabilities

### New Capabilities

None — these are extensions to existing view behavior.

### Modified Capabilities

- `tui-board`: Add `d` (mark done with confirmation) and `Del`/`Backspace` (delete with confirmation) to the Tabular view keyboard navigation requirement; add `Del`/`Backspace` (delete with confirmation) to the Closed view keyboard navigation requirement; add focus-restoration rules for both list views after delete/mark-done.

## Impact

- `src/knbn/views/_row_list.py` — base class likely needs the action bindings added or the subclasses override them
- `src/knbn/views/tabular.py` — add `action_mark_done` and `action_delete` bindings
- `src/knbn/views/done_week.py` — add `action_delete` binding
- `src/knbn/views/_row.py` — may need key-bindings forwarded
- `src/knbn/widgets/help.py` — update help overlay to list new key bindings for views 2 and 3
- `openspec/specs/tui-board/spec.md` — add requirements and scenarios for new actions in Tabular and Closed views
