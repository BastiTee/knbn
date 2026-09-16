## 1. Implementation

- [x] 1.1 Remove the `yield SystemCommand('Quit', 'Quit the application', self.action_quit)` line from `get_system_commands` in `src/knbn/app.py`
- [x] 1.2 Run `uv run knbn board`, open the command palette with `Ctrl+P`, and verify it lists only `Theme` and `Keys` (no `Quit`), and that `q` still quits the app from the footer/keybinding
- [x] 1.3 Run `uv run mypy src/` and `uv run ruff check src/ tests/` and verify both pass

## 2. Validation

- [x] 2.1 Run `uv run pytest tests` and verify the full suite passes
- [x] 2.2 Run `openspec validate remove-quit-from-palette --strict` and verify it passes
