## Why

The existing workflow splits task management across two contexts: tasks are captured in the terminal but then managed in Notion via a browser. Every review, status change, or reprioritization forces a context switch out of the terminal. `knbn` eliminates this by providing a full-lifecycle Kanban board that runs entirely in the terminal.

## What Changes

- **New CLI entry point**: `knbn` command (replaces placeholder `knbn_cli`)
- **New TUI board**: Full interactive Kanban board with three views (Kanban, Tabular, Done-by-Week)
- **New quick-add command**: `knbn add` with interactive prompts and shortcut flags
- **New data layer**: CSV-backed task store + per-task Markdown notes in `~/.knbn/`
- **New task model**: Dataclass representing all 10 task fields from the Notion schema
- **Replaces placeholder boilerplate**: `src/knbn/__init__.py` and `src/knbn/__main__.py` are replaced with real implementation
- **New dependencies**: `textual` and `click` added to `[project.dependencies]`

## Capabilities

### New Capabilities

- `task-model`: The core `Task` dataclass with all fields, status/priority enums, and validation
- `task-store`: CSV-backed persistence layer — load, save, add, update, delete tasks; Markdown notes management
- `cli-add`: `knbn add` subcommand for quick terminal-native task capture with configurable prompts and shortcut flags
- `tui-board`: Interactive TUI application (Textual) with Kanban, Tabular, and Done-by-Week views
- `task-notes`: Per-task Markdown notes — slug-based filenames, `$EDITOR` integration, presence indicator on cards

### Modified Capabilities

## Impact

- `pyproject.toml`: entry point renamed from `knbn_cli` to `knbn`; `textual>=0.80.0` and `click>=8.1.0` added to dependencies; coverage omit list expanded to exclude TUI modules
- `src/knbn/`: all existing files replaced; new module tree added under `model/`, `views/`, `widgets/`
- `tests/`: existing placeholder test replaced; new test modules added for store, slug, and CLI
- No external APIs; no database; no network dependencies
