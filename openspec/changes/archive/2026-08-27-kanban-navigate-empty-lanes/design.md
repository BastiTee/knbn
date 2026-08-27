## Context

`KanbanView._focus_col_card()` calls `_get_cards_in_col()` and returns early if the result is empty. This causes `action_focus_left` and `action_focus_right` to silently do nothing when the target column has no task cards. Combined with the recent lane-context feature, this means the user can never reach an empty lane to create a task there from the board.

## Goals / Non-Goals

**Goals:**
- When navigating into an empty column, focus the topmost visible `LaneHeader` in that column so the user has a visible focus target.
- Preserve `get_lane_context()` behaviour — it already reads `LaneHeader._priority` and maps `_focused_col` to status, so no changes needed there.

**Non-Goals:**
- Changing up/down behaviour inside an empty column (no-op is correct — nothing to move between).
- Changing the board layout or adding placeholder widgets.

## Decisions

**Focus the first `LaneHeader` when a column is empty**

`_focus_col_card()` gains a fallback: if `_get_cards_in_col()` returns nothing, query `LaneHeader` widgets inside `#col-{_focused_col}` and focus the first one. This is a one-path addition — the happy path (cards exist) is unchanged.

Alternative considered: focus any first focusable widget in the column via Textual's tab order. Rejected — too indirect; explicitly targeting `LaneHeader` is clear and consistent with how `get_lane_context()` already interprets a focused header.

## Risks / Trade-offs

- None significant. `LaneHeader.can_focus = True` is already set; this just uses it as a fallback target.
