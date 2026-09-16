## 1. Refocus helper and lane-toggle fix

- [x] 1.1 Add `_refocus_after_mutation(col_idx, old_card_row)` private method to `KanbanView` in `kanban.py`: after recompose, focus the card at `min(old_card_row, len(col_cards) - 1)` in the given column; if no cards remain, focus the first visible `LaneHeader` in that column. Verify by manual inspection that the method handles empty-column edge case.
- [x] 1.2 Fix `on_lane_header_toggled` in `kanban.py`: capture the priority label of the toggled header and the column index before calling `recompose()`, then schedule a `call_after_refresh` callback that queries the new `LaneHeader` with that priority in that column and calls `.focus()` on it. Verify by running `uv run knbn board`, toggling a lane header, and confirming the same header stays focused (no Tab needed).

## 2. Delete and mark-done focus restoration

- [x] 2.1 Fix `action_delete_task` in `kanban.py`: before showing the confirm dialog, capture the column index and the flat card row within that column (index of the focused card in `_get_cards_in_col`). In the `on_confirm` callback, after scheduling `recompose`, schedule a second `call_after_refresh` that calls `_refocus_after_mutation(col_idx, card_row)`. Verify by deleting a mid-list card and confirming focus lands on the next card without pressing Tab.
- [x] 2.2 Fix `_set_status` in `kanban.py` (used by mark-done): before recomposing, capture the column index and card row of the focused task. After the existing `call_after_refresh(self.recompose)`, schedule a second `call_after_refresh` that calls `_refocus_after_mutation(col_idx, card_row)`. Verify by marking a task done and confirming focus lands on the next card without pressing Tab.

## 3. Spec sync and edge-case verification

- [ ] 3.1 Manually verify all eight scenarios from the delta spec: (a) lane collapse keeps header focused, (b) lane expand keeps header focused, (c) delete with card below, (d) delete of last card (card above gets focus), (e) delete of only card in column (lane header gets focus), (f) mark-done with card below, (g) mark-done of last card, (h) mark-done of only card. Run `uv run knbn board` against `tests/fixtures/tasks.csv` data to exercise each case.
- [x] 3.2 Run `make build` (test + mypy + lint + format) and confirm it passes cleanly.
