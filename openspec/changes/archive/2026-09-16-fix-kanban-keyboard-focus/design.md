## Context

See proposal.md – Why for motivation. The root cause is that `KanbanView.recompose()` destroys and recreates all child widgets. Any widget that held focus ceases to exist, leaving Textual with no focused widget. The three affected code paths are:

- `on_lane_header_toggled` — calls `await self.recompose()` directly
- `_set_status` (used by mark-done) — calls `self.call_after_refresh(self.recompose)`
- `action_delete_task` on-confirm callback — calls `self.call_after_refresh(self.recompose)`

## Goals / Non-Goals

**Goals:**
- Restore keyboard focus automatically in all three board-mutation paths
- Keep the fix minimal and localised to `kanban.py`

**Non-Goals:**
- Focus restoration in Tabular or Closed views (they are not affected)
- General Textual focus management beyond these three cases

## Decisions

### Decision: capture focus intent before recompose, then apply after

After recompose, the previously-focused widget no longer exists. The fix is to record enough information to identify the *intended* post-recompose focus target before calling recompose, then schedule a `call_after_refresh` callback that finds the new widget matching that intent and calls `.focus()` on it.

**Lane toggle**: capture the priority label of the toggled `LaneHeader`. After recompose, find the `LaneHeader` with that same priority in the same column and focus it.

**Task deletion / mark-done**: capture the column index and the flat card index within the column (counting top-to-bottom across swimlanes). After recompose, focus the card at `min(captured_row, new_column_length - 1)`. If the column has no cards, focus the first visible `LaneHeader` in that column.

Alternative considered: Focus the nearest focusable element using Textual's built-in `focus_next()` / `focus_previous()`. Rejected because those methods traverse the entire app focus order and can land on a widget in a different column or outside the board, which is disorienting.

### Decision: extract a shared `_refocus_after_mutation` helper

Both deletion and mark-done share the same post-mutation focus rule. Extract it as a private helper `_refocus_after_mutation(col_idx, card_row)` that is called from the `call_after_refresh` chain in both places, to avoid duplicating the rule.

## Risks / Trade-offs

- [Risk] The lane header priority lookup could fail if the priority string changes case between widgets → use exact `_priority` attribute matching (which is already used in `_focus_same_priority_header`).
- [Risk] `call_after_refresh` ordering: if two callbacks are queued, the order must be `recompose` first, then `_refocus`. The current codebase already follows this pattern in `_move_task` and `_swap_in_lane` — the same ordering is safe to apply here.
