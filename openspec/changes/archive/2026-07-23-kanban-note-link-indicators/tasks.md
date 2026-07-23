## 1. Update card indicators

- [x] 1.1 Rename `_notes_indicator()` to `_card_indicators()` in `src/knbn/widgets/card.py` and update it to return `☰` when notes exist, `※` when `key_resource` is set, `☰ ※` when both, and `''` when neither
- [x] 1.2 Update the caller in `TaskCard.compose()` to use `_card_indicators()`

## 2. Add open-URL keybinding to Kanban view

- [x] 2.1 Add `Binding('o', 'open_url', 'Open URL', show=False)` to `KanbanView.BINDINGS` in `src/knbn/views/kanban.py`
- [x] 2.2 Implement `action_open_url()` in `KanbanView`: get focused card's `knbn_task.key_resource`, call `subprocess.run(['open', url], check=False)` if non-empty, no-op otherwise

## 3. Validate and test

- [x] 3.1 Run `uv run pytest tests` and confirm all tests pass
- [x] 3.2 Run `uv run mypy src/` and confirm no type errors
- [x] 3.3 Run `uv run ruff check src/ tests/` and fix any lint issues
