## 1. Add keyboard shortcut to TaskForm

- [x] 1.1 Add `Binding('ctrl+s', 'save', 'Save', show=True)` to `TaskForm.BINDINGS` in `src/knbn/widgets/form.py`
- [x] 1.2 Add `action_save(self)` method that calls `self._save()`

## 2. Verify

- [x] 2.1 Run `uv run mypy src/` and `uv run ruff check src/` — no errors
- [x] 2.2 Run `uv run pytest tests/` — all passing
