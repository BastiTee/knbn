## Context

All three views (`KanbanView`, `TabularView`, `ClosedView`) receive a `list[Task]` from the app at mount time and rebuild their widget trees from scratch on every `recompose()`. Navigation in the list views (`TabularView`, `ClosedView`) is index-based into `self._rows: list[TaskRow]`; in `KanbanView` it's position-based in `TaskCard` children of column containers. See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- `Ctrl+F` activates a visible search bar; `Esc` (or a second `Ctrl+F`) deactivates it.
- Letter/number keys append to the query while search is active; bindings for `1/2/3/q/r/a/n/d/o/…` are suppressed.
- Arrow keys, Enter, PgUp/PgDn, Delete continue to work — navigating the visible filtered subset.
- Filter applies to all three views with no disk I/O on each keystroke.
- Search state survives view switches and opening/closing the task form.

**Non-Goals:**
- Regex or multi-token search.
- Highlighting matched text within task cards/rows.
- Searching key_resource, due date, status, or priority fields.
- Fuzzy/approximate matching.

## Decisions

### App-level `_on_key` (capture phase) for key routing

`KnbnApp._on_key` fires before any widget or binding in Textual's capture phase. When search is active and `len(screen_stack) == 1` (no modal open):
- **Printable character** (`event.character.isprintable()`) → append to `_search_query`, stop event.
- **Backspace** → remove last char, stop event.
- **Esc** → deactivate search, stop event.
- **Everything else** (arrows, Enter, Delete, Ctrl+…) → not stopped, reaches views and their bindings normally.

`len(screen_stack) == 1` guard ensures that when a modal (TaskForm, ConfirmDialog, etc.) is open, Esc dismisses the modal and character keys are not captured by the search — they go to the modal as expected.

_Alternative considered_: Use a real `Input` widget with a custom key override. Rejected because arrow keys in a standard `Input` move the cursor rather than navigating tasks, requiring complex focus juggling between the input and the view.

### SearchBar as a display-only `Static`, not an `Input`

`SearchBar` in `src/knbn/widgets/search_bar.py` is a `Static` widget that renders `/ {query}▋`. The App updates it by calling `search_bar.update(text)` after every `_search_query` change. No focus, no event handling.

_Alternative considered_: Render the query inside an extended `KnbnFooter`. Rejected to keep the footer class simple and because adding a separate `SearchBar` is easier to show/hide (`display: none` ↔ `block`).

### Filter applied during `compose()` in each view

Each view reads `getattr(self.app, '_search_query', '')` during `compose()`. Non-matching tasks are skipped. The global `task_index` map (`{id(t): i for i, t in enumerate(self._tasks)}`) is built from the FULL `self._tasks` list so that `TaskRow.task_index` and `card-{idx}` IDs always refer to correct CSV row numbers even when the display list is filtered.

`_refilter_view()` in `KnbnApp` calls `call_after_refresh(view.recompose)` — no `_reload_tasks()` (no disk I/O).

_Alternative considered_: Pass a pre-filtered subset as `_tasks` to the view. Rejected because it breaks the index-to-CSV mapping used by edit/delete operations.

### Placement: between `#view-container` and `KnbnFooter`

```
Screen
  Static#view-container  (height: 1fr)
  SearchBar#search-bar   (height: 0/1, display: none/block)
  KnbnFooter
```

In Kanban mode the `#archive-bar` is inside `KanbanView` (inside `#view-container`), so the visual order becomes: board content → archive bar → search bar → footer. The archive bar is _above_ the search bar, not below it. This is acceptable given the architectural simplicity it preserves; moving the archive bar out of `KanbanView` would be a more invasive refactor.

### Filter function in `src/knbn/views/_filter.py`

Shared by all three views. Case-insensitive substring check across `title`, `category`, `free_text_1`, `free_text_2`, `free_text_3`.

## Risks / Trade-offs

- **Frequent recompose on keystroke**: Every character appended triggers `recompose()` on the current view. For typical board sizes (< 200 tasks) this is imperceptible. If it becomes a problem, a debounce (`set_timer`) can be added later.
- **`_on_key` capture phase**: Overriding `_on_key` on the App is non-standard and could interact with future Textual upgrades. The `await super()._on_key(event)` call at the end preserves all default App behaviour.
- **Focus jumps to first item on each refilter**: `recompose()` triggers `on_mount` which focuses the first visible item. Preserving the previous cursor position across filter changes is intentionally deferred.
