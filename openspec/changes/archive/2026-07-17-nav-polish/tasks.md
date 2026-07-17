## 1. Remove manual on_key relay from child widgets

- [x] 1.1 Delete the `on_key` method from `TaskCard` (`src/knbn/widgets/card.py`) — this removes the ancestor-walking Shift+arrow relay that causes double-dispatch in the Kanban view
- [x] 1.2 Add Tab/Shift+Tab suppression back to `TaskCard.on_key` (replace the deleted method with a minimal one that only stops Tab)
- [x] 1.3 Delete the `on_key` method from `TaskRow` (`src/knbn/views/_row.py`) — removes the ancestor-walking relay for Tabular/Done views
- [x] 1.4 Add Tab/Shift+Tab suppression back to `TaskRow.on_key`

## 2. Verify Shift+arrow bindings reach views

- [x] 2.1 Confirm `KanbanView.BINDINGS` already has `priority=True` on `shift+up` / `shift+down` / `shift+left` / `shift+right` — no change needed if so
- [x] 2.2 Confirm `TabularView.BINDINGS` has `priority=True` on `shift+up` / `shift+down` — add if missing
- [x] 2.3 Confirm `DoneByWeekView.BINDINGS` has `priority=True` on `shift+up` / `shift+down` — add if missing

## 3. Fix focus-follows-move in Kanban

- [x] 3.1 Verify that `_move_and_refocus` in `KanbanView` updates `_focused_col` and `_focused_row` and calls `_focus_col_card` inside the `refocus` closure — confirm both priority-change and status-change paths land focus on the moved card
- [x] 3.2 Manually trace a priority-change (Shift+↑ on a Medium card): after recompose, confirm `refocus` finds the card by title and calls `focus()` on it

## 4. Auto-focus on mount

- [x] 4.1 Verify `KanbanView.on_mount` calls `_focus_col_card` — confirm first card in first non-empty column is focused; fix if not
- [x] 4.2 Verify `TabularView.on_mount` focuses `self._rows[0]` — confirm it fires correctly after view switch
- [x] 4.3 Verify `DoneByWeekView.on_mount` focuses `self._rows[0]` — confirm it fires correctly after view switch

## 5. Tab suppression at view level

- [x] 5.1 Confirm `KanbanView.on_key` already suppresses Tab/Shift+Tab when the view widget has focus
- [x] 5.2 Confirm `TabularView.on_key` already suppresses Tab/Shift+Tab at the view level
- [x] 5.3 Confirm `DoneByWeekView.on_key` already suppresses Tab/Shift+Tab at the view level

## 6. Validation

- [x] 6.1 Run `uv run pytest tests` — all tests pass
- [x] 6.2 Run `uv run mypy src/` — no new type errors
- [x] 6.3 Run `uv run ruff check src/ tests/` — no new lint errors
- [ ] 6.4 Smoke-test in live TUI: Shift+↑/↓ on a Kanban card changes priority and keeps focus on the moved card
- [ ] 6.5 Smoke-test: Shift+↑/↓ in Tabular view skips 10 rows
- [ ] 6.6 Smoke-test: Tab does nothing in all three views
- [ ] 6.7 Smoke-test: switching views auto-focuses the first item
