## Context

`KanbanView.BINDINGS` already has `left`/`right`/`up`/`down` for navigation. Textual represents modifier keys in binding keys with a `shift+` prefix (e.g. `shift+up`). The board renders columns in `_STATUS_ORDER = ['Todo', 'Now', 'Feedback']` (col 0–2). `PRIORITY_VALUES = ['High', 'Medium', 'Low']` (index 0–2). `update_task(data_dir, idx, updated_task)` persists the change and `_reload_and_refocus` (or equivalent) recomposes the view.

## Goals / Non-Goals

**Goals:**
- `shift+up`/`shift+down` cycle through `PRIORITY_VALUES` (clamp at boundaries).
- `shift+left`/`shift+right` cycle through `_STATUS_ORDER` (clamp at boundaries — no escape to terminal statuses).
- Focus follows the moved card after recompose.

**Non-Goals:**
- Moving to `Done`, `Delegated`, or `Stopped` via Shift+arrow.
- Reordering within a swimlane (cards within a lane are sorted by `date_modified`, not positionally).
- Any animation or undo.

## Decisions

**Implement as four new action methods on `KanbanView`**

`action_move_up`, `action_move_down`, `action_move_left`, `action_move_right` mirror the existing `action_mark_done` / `action_move_status` pattern: get the focused task, mutate it, call `update_task`, reload, and re-focus.

**Focus recovery after recompose**

After `update_task` + `_reload_tasks` + `_show_view('kanban')`, the card at the same `(col, row)` position is focused via `_focus_col_card`. Since the card may shift position within a lane (sort order changes when `date_modified` updates on save), the simplest safe approach is to focus the first card in the target column — consistent with the current post-edit behaviour already in place for other mutations.

**Shift+left at `Todo` and Shift+right at `Feedback` are silent no-ops**

No toast or notification — the card simply doesn't move. This is consistent with how arrow navigation clamps at boundaries without any feedback.

## Risks / Trade-offs

- **Shift+up/down changes priority, not swimlane position**: the user asked for this explicitly. Within a swimlane, card order is driven by `date_modified` not an explicit rank, so "move higher in the lane" maps naturally to "increase priority".
- **No cross-lane positional memory after move**: the focused row resets to 0 in the target column. Acceptable for a move gesture.
