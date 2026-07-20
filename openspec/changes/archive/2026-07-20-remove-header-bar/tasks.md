## 1. Remove Header widget

- [x] 1.1 Remove `yield Header()` from `KnbnApp.compose()` in `src/knbn/app.py`
- [x] 1.2 Remove `Header` from the `from textual.widgets import ...` import line

## 2. Verify

- [x] 2.1 Run `uv run mypy src/` and `uv run ruff check src/` — no errors
- [x] 2.2 Run `uv run pytest tests/` — all passing
