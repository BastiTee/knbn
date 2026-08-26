## Why

The current TUI has two overlapping interactions — `Enter` opens a read-only task detail panel, and `e` opens the edit form — which forces an unnecessary two-step workflow to edit a task and creates inconsistency between views (the detail panel exists but the edit form is the real working surface). Collapsing these into a single action reduces friction and makes the keybinding model simpler and uniform across all three views.

## What Changes

- `Enter` on any focused task (Kanban card, Tabular row, Closed row) now opens the **edit form** directly instead of the read-only detail panel.
- The read-only task detail panel (`TaskDetailPanel` modal) is **removed entirely**.
- The `e` shortcut is **removed** from all views and from the now-gone detail panel.
- The help overlay and spec language are updated to reflect the new single-action model.
- All three views (Kanban, Tabular, Closed) behave identically: `Enter` = edit.

## Capabilities

### New Capabilities
- none

### Modified Capabilities
- `tui-board`: Requirements for keyboard navigation on board, tabular view, closed view, task detail panel, and inline add/edit form all change — `Enter` triggers the edit form everywhere; the detail panel requirement is removed; `e` is removed from all keybinding tables.

## Impact

- `src/knbn/views/kanban.py` — remove `Enter`→detail, remove `e`→edit; wire `Enter`→edit form
- `src/knbn/views/tabular.py` — change `Enter` from detail to edit form
- `src/knbn/views/done_week.py` — change `Enter` from detail to edit form
- `src/knbn/views/_row.py` / `_row_list.py` — update keybinding declarations
- `src/knbn/app.py` — remove detail panel handlers; `Enter` dispatches `TaskForm` in all views
- `src/knbn/widgets/detail.py` — file can be deleted
- `src/knbn/widgets/help.py` — remove `Enter`/`e` descriptions; add single `Enter` = edit entry
