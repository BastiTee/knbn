## Why

The knbn TUI has no way to narrow down a large task list. Users must scroll and visually scan all tasks. A live search filter lets users jump to relevant tasks instantly, which is especially valuable when the board has many items across multiple statuses.

## What Changes

- `Ctrl+F` activates a search bar that appears above the footer in all three views (Kanban, Tabular, Closed).
- Typing filters tasks in real time by title, category, and the three free-text fields.
- Non-matching tasks are hidden; navigation behaves exactly as if they don't exist.
- `Esc` clears the filter and restores all tasks.
- Letter/number keys that normally trigger view actions (1/2/3, q, r, a, n, d, …) are disabled while search is active.
- Arrow keys, Enter, PgUp/PgDn, and Delete continue to work normally during search.
- Opening a task detail keeps the active search alive; the filter is restored when the form closes.

## Capabilities

### New Capabilities

- `task-search-filter`: Live substring filter across all three TUI views, activated and dismissed from the keyboard.

### Modified Capabilities

(none — no existing spec-level behavior changes)

## Impact

- **`src/knbn/app.py`** — `Ctrl+F` binding; `_on_key` override for key routing; `_search_active`/`_search_query` state; `SearchBar` in compose.
- **`src/knbn/widgets/search_bar.py`** (new) — `SearchBar(Static)` display widget.
- **`src/knbn/views/_filter.py`** (new) — `task_matches()` predicate.
- **`src/knbn/views/kanban.py`**, **`tabular.py`**, **`done_week.py`** — read `_search_query` from app and filter during `compose()`.
