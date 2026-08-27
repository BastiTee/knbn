## Why

When adding a task from the Kanban board, the user is already positioned in a specific lane (a priority row + status column intersection, e.g., High+Todo). Requiring them to re-select those values in the form is redundant friction — the context is already there.

## What Changes

- Pressing `a` on the Kanban board now opens the add form with Status and Priority pre-populated from the focused lane/column position.
- The form remains editable — pre-population is a convenience default, not a lock.
- No change to `a` behaviour in Tabular or Closed views (no lane context there).

## Capabilities

### New Capabilities

_(none — this enhances existing behaviour)_

### Modified Capabilities

- `tui-board`: The "Inline add/edit form" requirement gains a new scenario: pressing `a` in the Kanban view pre-populates Status and Priority from the current focused cell's column (status) and swim lane row (priority).

## Impact

- `src/knbn/views/kanban.py` — must determine the focused cell's status/priority and pass them when opening the form.
- `src/knbn/widgets/form.py` — `TaskForm` must accept optional `initial_status` and `initial_priority` parameters and apply them as default selections.
- `src/knbn/app.py` — `on_task_form_task_saved` / add-form dispatch may need to thread the context through.
- No CSV schema changes. No new dependencies.
