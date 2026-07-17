## Context

The `knbn` project is a Python CLI/TUI package. Its skeleton exists (uv build, ruff, mypy, pytest) but contains only placeholder boilerplate. This design covers the initial full implementation: replacing the boilerplate with a real task management tool.

The existing Notion workflow uses a CSV-exported schema as the data format. Preserving that schema exactly means zero migration cost for existing data.

## Goals / Non-Goals

**Goals:**
- Replace placeholder boilerplate with a working CLI + TUI
- Persist tasks as a human-readable, Notion-compatible CSV
- Provide `knbn add` for fast terminal capture and `knbn board` for full lifecycle management
- Keep the dependency surface minimal (only `click` and `textual`)
- Maintain ≥95% test coverage on the non-TUI modules

**Non-Goals:**
- Mouse support
- Cross-platform (Windows) compatibility
- Sync with Notion or any external service
- Multi-user or concurrent access
- Plugin/extension system

## Decisions

### D1: Textual for TUI
**Decision**: Use the `textual` library for the TUI.  
**Rationale**: Textual provides a reactive widget system, CSS-based layout, keyboard event handling, and terminal resize events out of the box. Building these from scratch with `curses` would take significantly longer with no benefit.  
**Alternatives considered**: `curses` (too low-level), `urwid` (older API, less active), `rich` alone (not a full TUI framework).

### D2: click for CLI layer
**Decision**: Use `click` for CLI argument/command parsing.  
**Rationale**: Matches the pattern in the existing `notion_task.py` the user already has; clean API for subcommands, prompts, and flag handling.  
**Alternatives considered**: `argparse` (no built-in prompt support), `typer` (wraps click but adds weight).

### D3: CSV as the only storage format
**Decision**: Store all tasks in a single `tasks.csv`. No SQLite, no JSON.  
**Rationale**: Human-readable, directly importable from Notion, diff-able in git, zero schema migration. Acceptable for a single-user personal tool.  
**Trade-off**: No indexed queries; the full file is loaded on every operation. Acceptable at personal-scale task counts (<10,000 rows).

### D4: No UUID / task identity by row index
**Decision**: Tasks are identified by their row index in the CSV. No UUID field.  
**Rationale**: Keeps the CSV schema identical to Notion's export. A personal tool with a single writer has no concurrent-edit conflicts that require stable IDs.  
**Trade-off**: Row indices shift on delete. The TUI always reloads from disk before acting, so stale indices are not an issue in practice.

### D5: TUI modules excluded from unit test coverage
**Decision**: `app.py`, `views/`, and `widgets/` are omitted from pytest coverage.  
**Rationale**: Textual widget behavior is difficult to unit test without an async event loop and terminal emulator. The model and store layers (which carry the real business logic) are fully tested.  
**Trade-off**: TUI regressions must be caught manually or via future integration tests.

### D6: Atomic CSV writes via rename
**Decision**: Write to `.tasks.csv.tmp` then `os.rename()` to `tasks.csv`.  
**Rationale**: `os.rename()` is atomic on POSIX filesystems (macOS). Prevents partial writes from corrupting the task database.

### D7: Module structure separates model, views, widgets, CLI
**Decision**: Organize as `model/` (pure data), `cli.py` (Click commands), `app.py` + `views/` + `widgets/` (TUI).  
**Rationale**: The model layer must be importable without Textual (for CLI use and tests). Clean separation makes testing the non-TUI code straightforward.

## Risks / Trade-offs

- **CSV race condition on concurrent writes** → Mitigation: single-user tool; documented as unsupported. Atomic rename protects against crash-during-write only.
- **Textual version API churn** → Mitigation: pin `textual>=0.80.0`; review changelog on upgrades.
- **Date format parsing brittleness** → Mitigation: use `strptime` with exact format strings from the source data; catch `ValueError` and display raw string when parsing fails rather than crashing.
- **`$EDITOR` subprocess blocking TUI** → Mitigation: use Textual's `suspend()` context manager (available since Textual 0.55) to cleanly pause and resume the TUI around the editor subprocess.
- **Slug collision edge cases** → Mitigation: slug uniqueness is checked against the actual `notes/` directory listing, not an in-memory cache.

## Open Questions

- None blocking MVP. The spec and DESIGN.md together fully define scope.
