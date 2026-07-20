## 1. Track active view in app

- [x] 1.1 Add `_active_view: reactive[str] = reactive("kanban")` to `KnbnApp`
- [x] 1.2 Set `self._active_view = view` in `_show_view` whenever the view changes

## 2. Apply bold styling to active footer key

- [x] 2.1 Add a CSS rule to `KnbnApp.CSS` that makes the active tab key bold — use `app.add_class` / `remove_class` on the app root with classes `view-kanban`, `view-tabular`, `view-closed` driven by `watch__active_view`
- [x] 2.2 Write three CSS rules targeting the footer key for each active class (e.g. `.view-kanban Footer .footer--key--1 { text-style: bold; }`) — verify the correct Textual CSS selector for footer keys by inspecting the running app or the Textual source

## 3. Verify and test

- [x] 3.1 Launch `uv run knbn board` and confirm the active tab key is bold on startup (Kanban = `1`)
- [x] 3.2 Switch to views 2 and 3 and confirm the highlight follows
- [x] 3.3 Run `uv run ruff check src/` and `uv run mypy src/` — no new errors
