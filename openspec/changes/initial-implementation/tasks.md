## 1. Project Setup

- [ ] 1.1 Update `pyproject.toml`: rename entry point from `knbn_cli` to `knbn`, add `textual>=0.80.0` and `click>=8.1.0` to `[project.dependencies]`, expand `[tool.coverage.run] omit` to exclude `app.py`, `views/`, and `widgets/`
- [ ] 1.2 Run `uv sync` to install new dependencies and verify the lockfile updates
- [ ] 1.3 Create the module directory skeleton: `src/knbn/model/`, `src/knbn/views/`, `src/knbn/widgets/` — each with an empty `__init__.py`
- [ ] 1.4 Create `tests/fixtures/` and copy `_temp_/example-database-content.csv` there as `tasks.csv`

## 2. Data Model

- [ ] 2.1 Create `src/knbn/model/task.py`: define the `Task` dataclass with all 10 fields, `STATUS_ACTIVE`, `STATUS_TERMINAL`, `STATUS_VALUES`, `PRIORITY_VALUES`, and `DEFAULT_CATEGORIES` constants
- [ ] 2.2 Write `tests/test_task_model.py`: verify Task construction (required fields, all fields, defaults), constant values and ordering

## 3. Slug Utility

- [ ] 3.1 Create `src/knbn/model/slug.py`: implement `make_slug(title: str) -> str` (lowercase, spaces→hyphens, strip non-alphanumeric-hyphen, truncate at 60 chars) and `unique_slug(title: str, existing: set[str]) -> str` (appends `-2`, `-3` on collision)
- [ ] 3.2 Write `tests/test_slug.py`: test basic slug, special character stripping, 60-char truncation, and collision suffix logic

## 4. Config

- [ ] 4.1 Create `src/knbn/config.py`: implement `resolve_data_dir() -> Path` that reads `KNBN_DATA_DIR` env var or defaults to `~/.knbn/`
- [ ] 4.2 Write `tests/test_config.py`: test env var override and default path

## 5. Store Layer

- [ ] 5.1 Create `src/knbn/model/store.py`: implement `ensure_data_dir(data_dir: Path)`, `load_tasks(data_dir: Path) -> list[Task]`, `save_tasks(data_dir: Path, tasks: list[Task])` (atomic write via `.tmp` rename), `add_task(data_dir: Path, task: Task)`, `update_task(data_dir: Path, index: int, task: Task)`, `delete_task(data_dir: Path, index: int)`
- [ ] 5.2 Implement `get_notes_path(data_dir: Path, task: Task) -> Path` and `notes_exist(data_dir: Path, task: Task) -> bool` in `store.py`, using `slug.py` for filename derivation
- [ ] 5.3 Write `tests/test_store.py`: test CSV round-trip using the fixture file, atomic save (temp file rename), add/update/delete operations, notes path resolution, notes existence check

## 6. CLI Layer

- [ ] 6.1 Create `src/knbn/cli.py`: implement `init` command (create data dir, `tasks.csv`, `notes/`; idempotent), `board` command (placeholder that calls `app.run()`), and `add` command with the full prompt sequence (title, status, priority, category, key resource) and conditional prompts for `Feedback From` / `Delegated To`
- [ ] 6.2 Add all `knbn add` flags: `--title`, `--status-default`, `--priority-default`, `--category-default`, `--no-resource`, `--fast`/`-f`
- [ ] 6.3 Replace `src/knbn/__main__.py` with the click group dispatcher that calls `cli.py`; replace `src/knbn/__init__.py` to remove the `greet` stub
- [ ] 6.4 Write `tests/test_cli.py`: test `knbn init` (creates dir + files, idempotent), `knbn add` with all flag combinations using `CliRunner` and mocked `store.add_task`; verify confirmation message and stored field values

## 7. TUI Application Shell

- [ ] 7.1 Create `src/knbn/app.py`: subclass `textual.App`, wire the CSS/theme, implement view switching (`1`/`2`/`3` keys), global quit (`q`/`Ctrl+C`), global add (`a`), and terminal-size guard (exit with message if < 100×30)
- [ ] 7.2 Create `src/knbn/widgets/help.py`: key bindings help overlay widget, shown on `?` and dismissed with `Esc`/`?`

## 8. Task Card Widget

- [ ] 8.1 Create `src/knbn/widgets/card.py`: `TaskCard` widget rendering title (truncated), category tag (colored pill per category color map), due date (red/bold if overdue), notes indicator `[N]` when notes file exists; focused card gets highlighted border

## 9. Kanban View

- [ ] 9.1 Create `src/knbn/views/kanban.py`: `KanbanView` widget with 3-column × 3-row grid layout; equal column widths; column headers with status name + task count; swim lane headers with priority label + task count; archive counts (Done/Delegated/Stopped) in footer/sidebar
- [ ] 9.2 Implement collapsible swim lanes: Space/Enter on lane header toggles collapse state; collapsed lane shows header only
- [ ] 9.3 Implement keyboard navigation: `←`/`→` between columns, `↑`/`↓` within column, `Tab`/`Shift+Tab` across cards
- [ ] 9.4 Implement card actions: `Enter` opens detail panel, `e` opens edit form, `d` → Done, `x` → Stopped, `g` → Delegate (prompt for Delegated To), `m` → move (prompt for status), `p` → change priority (prompt), `Del`/`Backspace` → delete with confirmation

## 10. Task Detail Panel

- [ ] 10.1 Create `src/knbn/widgets/detail.py`: `TaskDetailPanel` widget showing all 10 task fields; keys `Esc`/`q` close, `e` opens edit form, `n` opens notes in `$EDITOR` (using Textual `suspend()`), `o` opens Key Resource URL via `subprocess` / `open`

## 11. Add/Edit Form

- [ ] 11.1 Create `src/knbn/widgets/form.py`: `TaskForm` overlay modal with fields in order (Title, Status, Priority, Category, Due, Key Resource, Feedback From, Delegated To); `Tab`/`Shift+Tab` navigation; conditional visibility of Feedback From / Delegated To; `Esc` cancels; submit saves via `store.update_task` or `store.add_task`

## 12. Tabular View

- [ ] 12.1 Create `src/knbn/views/tabular.py`: `TabularView` widget; active tasks grouped by status (`Now`, `Feedback`, `Todo`); within each group sorted by priority rank then `date_modified` descending; columns: Name (fills remaining), Priority, Category, Due

## 13. Done-by-Week View

- [ ] 13.1 Create `src/knbn/views/done_week.py`: `DoneByWeekView` widget; terminal-status tasks grouped by ISO week of `date_modified`, most recent week first; group header shows formatted date range + count; columns: Name, Category, Priority, Last edited time, Date Created

## 14. Notes Integration

- [ ] 14.1 Wire notes opening from the Kanban view (`n` key on focused card): suspend TUI, invoke `$EDITOR` (fallback `nano`) on the task's notes file (created if absent), resume TUI after editor exits
- [ ] 14.2 Ensure `TaskCard` re-queries notes existence after editor returns and updates the `[N]` indicator

## 15. Integration Smoke Test

- [ ] 15.1 Run `uv run knbn init` and verify `~/.knbn/` is created with correct structure
- [ ] 15.2 Run `uv run knbn add --fast --title "Test task"` and verify the row appears in `tasks.csv`
- [ ] 15.3 Run `uv run knbn board` and verify the TUI launches, shows the test task on the board, and quits cleanly on `q`
- [ ] 15.4 Run `uv run pytest` and verify all tests pass with ≥95% coverage on non-TUI modules
- [ ] 15.5 Run `uv run ruff check src/ tests/` and `uv run mypy src/` and verify no errors
