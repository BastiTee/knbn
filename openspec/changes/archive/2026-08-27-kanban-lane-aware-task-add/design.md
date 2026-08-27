## Context

`action_add_task` in `app.py` opens `TaskForm(data_dir=..., task=None)` with no pre-filled status or priority, so the form always defaults to `Todo` / `Medium`. When the user is on the Kanban board with a card focused in, say, the `High` row of the `Feedback` column, they already know the target lane — re-selecting it in the form is redundant.

## Goals / Non-Goals

**Goals:**
- Pre-populate Status and Priority in the add form when `a` is pressed from the Kanban view.
- Derive context from the focused card's task (status + priority) or from the focused lane header (priority) + column tracker (`_focused_col` → status).
- Keep the form fully editable — pre-population is a convenience default.

**Non-Goals:**
- Pre-population from Tabular or Closed views (no lane structure there).
- Changing any other form field defaults.
- Altering the `a` keybinding location (stays in `app.py`).

## Decisions

**1. Expose a `get_lane_context()` method on `KanbanView`**

`app.py` queries for `KanbanView` when in kanban mode and calls `get_lane_context() -> tuple[str, str] | None`. This returns `(status, priority)` or `None` if context cannot be determined. Keeps the app-level handler thin and avoids binding duplication.

Alternative considered: move the `a` binding into `KanbanView`. Rejected — `a` is a global binding on `KnbnApp` that works from all views; duplicating or overriding it would require priority gymnastics and introduce asymmetry.

**2. Determine context from focused widget**

Priority order:
1. If a `TaskCard` is focused → use `card.knbn_task.status` and `card.knbn_task.priority`.
2. If a `LaneHeader` is focused → use `_STATUS_ORDER[self._focused_col]` for status and `header._priority` for priority.
3. Fallback → return `None` (form uses its own defaults).

This covers the common cases (card focused, empty-lane header focused) without guessing.

**3. Add `initial_status` / `initial_priority` params to `TaskForm`**

`TaskForm.__init__` gains two optional `str | None` keyword args. `compose()` uses them as the default `Select` value only when `existing_task is None`. Existing call sites pass `task=None` with no extra args and are unaffected.

## Risks / Trade-offs

- If the focused widget is a `LaneHeader` in a collapsed lane, `_priority` is still accurate. No issue.
- If the board has no cards and no lane header is focused (edge case on first mount), `get_lane_context()` returns `None` and the form falls back to defaults. Acceptable.
- The `knbn_task` attribute is already the established pattern for `TaskCard` (per CLAUDE.md) — no naming conflict.
