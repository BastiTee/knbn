# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`knbn` is a terminal-native personal Kanban board. It replaces a Notion-based task management workflow with a fully terminal-native tool. The authoritative design specification is in `openspec/DESIGN.md`.

## Commands

```bash
uv run pytest tests                        # full test suite
uv run pytest tests/test_store.py -k foo  # single test
uv run mypy src/                           # type checking
uv run ruff check src/ tests/             # linting
uv run ruff check --fix src/ tests/       # auto-fix lint
uv run ruff format src/ tests/            # format
uv run knbn --help                         # CLI entry point
uv run knbn add --fast --title "My task"  # quick task add
uv run knbn board                          # launch TUI
make build                                 # full build chain (test + mypy + lint + format + uv build)
```

## Before committing

Always run `make format` before staging and committing. The build chain enforces formatting via `ruff format`; skipping it leaves violations that fail CI.

## Architecture

### Module layout

```
src/knbn/
  __main__.py        # entry point — dispatches to cli.py
  cli.py             # Click commands: init, board, add
  config.py          # resolve_data_dir(): KNBN_DATA_DIR env var or ~/.knbn/
  app.py             # Textual App — view switching, global keybindings
  model/
    task.py          # Task dataclass + STATUS_*/PRIORITY_VALUES/DEFAULT_CATEGORIES constants
    store.py         # CSV read/write (atomic via .tmp rename), notes path resolution
    slug.py          # title → filename slug, collision suffixes
  views/
    _columns.py      # shared column layout constants (FIXED_OVERHEAD, format helpers)
    _row.py          # TaskRow — focusable Static widget used in list views
    _row_list.py     # RowListView — base class for tabular/done_week with cursor + keybindings
    kanban.py        # 3×3 board (Todo/Now/Feedback × High/Medium/Low)
    tabular.py       # active tasks grouped by status
    done_week.py     # "Done" view (key 3) — archived tasks grouped by ISO calendar week
  widgets/
    _confirm.py      # ConfirmDialog — ModalScreen[bool], y/n/escape keybindings
    card.py          # TaskCard — uses knbn_task (not task) to avoid asyncio.Task clash
    detail.py        # TaskDetailPanel modal — uses knbn_task
    form.py          # TaskForm modal — posts TaskForm.TaskSaved message on save
    help.py          # HelpOverlay modal
```

### Data storage

Tasks live in `~/.knbn/tasks.csv` (override with `KNBN_DATA_DIR`). The CSV schema matches Notion's export format exactly — column order is canonical and must not change. Notes are Markdown files in `~/.knbn/notes/<slug>.md`, opened in `$EDITOR` (fallback: `nano`).

### Key design constraints

- **`task` attribute name is reserved** by Textual's `MessagePump`. Widgets store the knbn task as `self.knbn_task`.
- **`recompose()` is async** in Textual 8 — call it with `await` or `self.call_after_refresh(self.recompose)` from sync contexts.
- **`action_dismiss`** on `ModalScreen` subclasses must match the superclass signature: `def action_dismiss(self, result: None = None) -> None`.
- `LaneHeader.Toggled` is a nested `Message` class; the handler is `on_lane_header_toggled`.
- **`get_system_commands`** is overridden in `KnbnApp` to restrict the `Ctrl+P` command palette to `Theme → Quit → Keys` only. Screenshot and Maximize/Minimize are intentionally suppressed.
- The form posts `TaskForm.TaskSaved`; the app handles it via `on_task_form_task_saved`.

### Testing

`tests/fixtures/tasks.csv` is the canonical CSV fixture — 16 generic tasks covering all six statuses and three priorities. TUI modules (`app.py`, `views/`, `widgets/`) are excluded from coverage. The 95% coverage floor applies to model and CLI code only.

### Tooling

- **Build**: `uv` (lockfile: `uv.lock`)
- **Lint + format**: `ruff` — many rules enabled; see `[tool.ruff.lint]` in `pyproject.toml` for the ignore list (Textual-specific patterns like `RUF012`, `PLC0415` are suppressed)
- **Types**: `mypy` with strict settings (`disallow_untyped_defs = true`)
- **Pre-commit**: runs ruff + ruff-format + gitleaks on every commit
