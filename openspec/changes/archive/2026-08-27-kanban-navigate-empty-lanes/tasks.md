## 1. Fix empty-column navigation

- [x] 1.1 In `KanbanView._focus_col_card()`, add a fallback: when `_get_cards_in_col()` returns an empty list, query `LaneHeader` widgets inside `#col-{_focused_col}` and focus the first one (if any)
- [x] 1.2 Make `action_focus_up/down` navigate through ALL focusable elements in the column (LaneHeaders + TaskCards in DOM order), not just cards — so empty lanes are reachable by pressing up/down
- [x] 1.3 Make `action_focus_left/right` preserve context across columns: if a LaneHeader is focused, land on the same-priority LaneHeader in the target column; if a TaskCard is focused, keep existing card-index matching
