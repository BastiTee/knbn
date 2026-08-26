## Context

The TUI currently has two separate task interaction surfaces: a read-only `TaskDetailPanel` modal (opened with `Enter`) and an editable `TaskForm` modal (opened with `e`). This split was inherited from an early design where viewing and editing were considered distinct operations, but in practice the detail panel adds no unique value — the edit form already shows all fields. The duplication also means two codepaths to maintain and an inconsistent mental model for the user. The change removes the detail panel entirely and promotes `Enter` as the single, universal "open task" action across all three views.

## Goals / Non-Goals

**Goals:**
- Single keybinding (`Enter`) to open the edit form from all three views (Kanban, Tabular, Closed).
- Remove `TaskDetailPanel` and its widget file entirely.
- Remove `e` shortcut from all views.
- Consistent behaviour: the same key does the same thing regardless of which view is active.

**Non-Goals:**
- Changing the edit form itself (`TaskForm`) — its fields, validation, and save behaviour are unchanged.
- Adding any new keyboard shortcuts or interaction modes.
- Altering the add (`a`) workflow.

## Decisions

**Reuse `TaskForm` unchanged as the single task-opening surface.**
The form already renders all task fields and supports editing. Routing `Enter` to `TaskForm` (pre-populated with the focused task) covers 100% of what the detail panel offered, with zero new code for the display side.

**Delete `detail.py` rather than repurposing it.**
The detail panel has no remaining responsibilities after this change. Keeping a stub would be dead code; removing it keeps the widget directory clean and prevents future confusion.

**Wire `Enter` → edit form at the view level, not in `_row.py`.**
Each view (`kanban.py`, `tabular.py`, `done_week.py`) already owns its `on_key` / `action_*` handlers. Binding `Enter` at the view level keeps the row widget (`_row.py`) generic and avoids coupling it to the form module.

**Remove `e` from the help overlay entry table.**
The help overlay lists all bindings. Removing `e` and consolidating to a single `Enter = Edit task` entry keeps the overlay accurate.

## Risks / Trade-offs

- [Muscle memory] Users accustomed to `e` for edit will need to retrain to `Enter`. → Mitigation: `Enter` is the more natural "open" key and was already wired to an action; the change is an upgrade, not a replacement with a new key.
- [Notes shortcut in detail panel] The detail panel exposed `n` to open notes. That shortcut already exists globally (`n` in the board view). → Mitigation: verify `n` is reachable in all views after this change; no new wiring needed.
- [Delete shortcut in detail panel] `Del`/`Backspace` in the detail panel triggered delete. That shortcut exists directly on Kanban cards too. → Mitigation: confirm delete is still reachable from Tabular/Closed views via the edit form's own delete action if present, or document that delete is Kanban-only.
