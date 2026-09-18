## 1. Filter predicate

- [x] 1.1 Create `src/knbn/views/_filter.py` with `task_matches(task: Task, query: str) -> bool` — case-insensitive substring check across `title`, `category`, `free_text_1`, `free_text_2`, `free_text_3`. Returns `True` when `query` is empty. Verify with a unit test in `tests/test_filter.py` covering title, category, free-text, case-insensitivity, and empty-query pass-through.

## 2. SearchBar widget

- [x] 2.1 Create `src/knbn/widgets/search_bar.py` with `SearchBar(Static)`. Default CSS: `height: 1; display: none; background: $primary-darken-2; padding: 0 1`. CSS class `--active` switches to `display: block`. No focus, no event handling — purely a display widget updated by the app via `self.update(text)`. Verify by importing in Python without errors.

## 3. App integration

- [x] 3.1 Add `_search_active: bool = False` and `_search_query: str = ''` to `KnbnApp.__init__`. Add `Binding('ctrl+f', 'toggle_search', 'Find', show=True)` to `BINDINGS`. Add `SearchBar(id='search-bar')` to `compose()` between `#view-container` and `KnbnFooter`. Verify the app still launches with `uv run knbn board`.

- [x] 3.2 Override `async def _on_key(self, event: Key) -> None` in `KnbnApp`. When `_search_active` and `len(screen_stack) == 1`: stop and handle printable chars (append), backspace (delete last), and Esc (deactivate); let all other keys pass through. Add `action_toggle_search`, `_activate_search`, `_deactivate_search`, `_update_search_bar`, `_refilter_view`. Do NOT call `super()._on_key` — this causes double-dispatch of key events through Textual's pipeline. Verify with manual testing: Ctrl+F opens bar, typing appends to query display, Esc closes, 'q' does not quit.

## 4. View filtering

- [x] 4.1 In `src/knbn/views/_filter.py`, confirm `task_matches` is importable. In `TabularView.compose()` add `_search_query` property and apply `task_matches` when building each status group. Verify: with search active and query matching only some tasks, only matching rows appear in tabular view.

- [x] 4.2 In `ClosedView.compose()` apply `task_matches` when building the terminal task list. Verify: filtering works in closed view.

- [x] 4.3 In `KanbanView._tasks_for()` and `_count_for_status()` apply `task_matches`. Verify: filtered cards and updated counts appear in kanban view; switching views preserves the active query.

## 5. Build and final verification

- [x] 5.1 Run `make build` (tests + mypy + lint + format) and confirm it passes with no new errors. (175 tests pass, 96.21% coverage)

