## Context

The TUI has three views (Kanban, Tabular, Done-by-week). Navigation is keyboard-only. Two bugs exist:

1. **Shift+arrow double-dispatch in Kanban**: `TaskCard.on_key` manually calls `ancestor.action_move_up/down`, AND the view also has `priority=True` bindings for `shift+up`/`shift+down`. When a `TaskCard` is focused, both paths fire — or the `priority=True` binding on the view intercepts before `on_key` on the card, depending on Textual's event-routing order. Result: the action either misfires or focus is lost after the recompose.

2. **Shift+arrow double-dispatch in Tabular/Done views**: `TaskRow.on_key` manually calls `ancestor.action_cursor_up/fast`. The view also has `priority=True` bindings. Same double-dispatch problem — `shift+up`/`shift+down` may be consumed by the binding layer before `on_key` runs, or run twice.

3. **Auto-focus on mount**: `on_mount` already exists in all three views and focuses the first item, but it does not re-run when the app replaces the view widget via `_show_view`. The view is freshly mounted each time, so `on_mount` should fire — however, focus may land on the wrong widget if Textual's default Tab-order steals it first.

4. **Tab key**: `on_key` in each view calls `event.prevent_default()` + `event.stop()` for `tab`/`shift+tab`, but this only works if the view widget itself has focus, not when a child card/row is focused.

## Goals / Non-Goals

**Goals:**
- Shift+arrow fires exactly once per keypress in all views
- First interactive item is focused immediately on mount (and on view switch)
- Tab and Shift+Tab do nothing in all three views regardless of which widget is focused
- After a Shift+arrow move on the Kanban board, focus lands on the moved card in its new position

**Non-Goals:**
- Mouse navigation
- Changing any other keybindings not related to the four items above
- Modifying the detail panel, form, or help overlay navigation

## Decisions

### Remove the manual `on_key` relay in `TaskCard` and `TaskRow`

The `on_key` in `TaskCard` and `TaskRow` manually walks ancestors to call `action_move_up` etc. This is redundant when the parent view already has `priority=True` bindings. The correct fix is to **delete the `on_key` methods** from both widgets and rely solely on Textual's binding system, which routes `shift+up`/`shift+down` to the nearest ancestor that declares those bindings (with `priority=True` ensuring they win over default Textual actions).

Alternative considered: keep `on_key` and remove the view-level bindings. Rejected — bindings declared in `BINDINGS` are the idiomatic Textual pattern and display in the footer; manual ancestor-walking is a workaround that fights the framework.

### Suppress Tab at the child widget level

Each focusable child widget (`TaskCard`, `TaskRow`) must suppress Tab in its own `on_key`. The parent's `on_key` is only called when the parent has focus; when a child is focused, the child's `on_key` fires first. Adding Tab suppression to `TaskCard` and `TaskRow` is the minimal fix.

Alternative considered: set `BINDINGS` with a no-op Tab action on every widget. This works but is more verbose and shows a footer entry. Suppressing in `on_key` keeps it invisible.

### Focus-follows-move via `call_after_refresh` chaining

`_move_and_refocus` already calls `recompose` then `refocus` via two `call_after_refresh` calls. The bug is that `refocus` searches by title match against the reloaded task list, but after a priority change the card's column stays the same while the row index changes — and the search correctly finds the new row. For a status change (Shift+left/right), the target column changes and the search should work. The fix is to ensure `_focused_col` and `_focused_row` are updated inside `refocus` before calling `_focus_col_card`, which the current code does. The actual bug is that the `priority=True` binding and the `on_key` relay both fire, causing `_move_and_refocus` to run twice — fixing the double-dispatch (decision 1 above) resolves this.

## Risks / Trade-offs

- [Removing `on_key` from `TaskCard`/`TaskRow`] → These methods also stopped Tab propagation for the card/row specifically. That Tab suppression must be added back as a separate `on_key` that only handles Tab. Otherwise Tab could shift focus away unexpectedly.
- [Relying on `priority=True` bindings] → If Textual changes its binding priority model in a future version, the fix may need revisiting. Acceptable for now; the current Textual 8 model is stable.
