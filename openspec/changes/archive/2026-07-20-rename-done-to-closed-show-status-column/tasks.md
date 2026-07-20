## 1. Rename view class and update row layout

- [x] 1.1 In `src/knbn/views/done_week.py`, rename class `DoneByWeekView` → `ClosedView` and update the module docstring
- [x] 1.2 In `src/knbn/views/done_week.py`, add `task.status` to `row_text` (insert after name, before category); adjust name truncation to 30 chars and field widths to fit 100-column terminal

## 2. Update app wiring

- [x] 2.1 In `src/knbn/app.py`, rename binding label `'Done'` → `'Closed'` for key `3`
- [x] 2.2 In `src/knbn/app.py`, rename action `action_show_done_week` → `action_show_closed` and view key `'done_week'` → `'closed'`; update the import of `DoneByWeekView` → `ClosedView`

## 3. Update help overlay

- [x] 3.1 In `src/knbn/widgets/help.py`, update the `3` binding description from `Done-by-week view` to `Closed view`

## 4. Update canonical spec

- [x] 4.1 In `openspec/specs/tui-board/spec.md`, replace the "Done view" requirement with "Closed view" (add Status column, update all label references from "Done" to "Closed")
- [x] 4.2 In `openspec/specs/tui-board/spec.md`, update the "View switching" requirement to reference `3 Closed` instead of `3 Done`
