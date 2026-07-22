## Context

Both table views (`TabularView`, `ClosedView`) share a column formatter in `src/knbn/views/_columns.py`. The title column is currently hard-coded to 28 characters. Fixed columns (status 11, priority 9, category 14, created 16, edited 16, due 10, leading padding 2, separating spaces 6) sum to ~84 characters of overhead, meaning a 120-column terminal wastes 36 characters that could be title.

Textual widgets expose `self.size.width` once mounted, and `on_resize` / `watch_*` hooks allow reactive re-render.

## Goals / Non-Goals

**Goals:**
- Title column fills all horizontal space not claimed by fixed columns.
- Minimum title width of 20 characters (prevents unreadable columns on narrow terminals).
- Header row and data rows stay aligned.

**Non-Goals:**
- Collapsible or re-orderable columns.
- Per-column resizing by the user.
- Changes to the kanban board view.

## Decisions

### Dynamic width calculation in `_columns.py`

`format_row` and the header builder gain a `title_width: int` parameter. The caller computes:

```
title_width = max(20, available_width - FIXED_COLS_WIDTH)
```

where `FIXED_COLS_WIDTH` is a module-level constant (sum of all non-title column widths including padding).

**Alternative considered**: compute width inside `_columns.py` by importing Textual's `App` reference. Rejected — tight coupling, hard to test.

### Width source in views

`RowListView` (base class) already inherits from `ScrollableContainer`. The `on_resize` event fires whenever the widget resizes. Override `on_resize` in both views to call `self.call_after_refresh(self._rebuild)` which triggers a `recompose()`. During `compose()`, use `self.size.width` (defaults to 0 before first mount, so clamp to min width).

**Alternative considered**: Pass width to `TaskRow` and format there. Rejected — `TaskRow` is a `Static`, formatting is already delegated to `_columns.py`; it's cleaner to keep the formatter stateless.

### No changes to `TaskRow`

`TaskRow` receives a pre-formatted string. The width dependency lives one level up, in the view's `compose()`.

## Risks / Trade-offs

- [Width = 0 before first mount] → Guard with `max(MIN_TITLE_WIDTH, self.size.width - FIXED_COLS_WIDTH)`. The initial render at width 0 produces minimum-width titles; on first resize event the view recomposes correctly.
- [Recompose on every resize] → `recompose()` is lightweight for these views (no async I/O). Acceptable.
- [FIXED_COLS_WIDTH constant drifts if columns change] → Defined once in `_columns.py` as a named constant alongside the format string, so any column change is local.
