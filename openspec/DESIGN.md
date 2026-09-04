# knbn — Design Document

> **Purpose of this document**: Authoritative, agent-readable specification for implementing the `knbn` terminal Kanban tool. Every implementation decision should trace back to a section here. When this document and a source comment disagree, this document wins until explicitly updated.

---

## 1. Project Overview

`knbn` is a terminal-native personal Kanban board written in Python. It replaces a Notion-based workflow where tasks are captured via CLI but managed in a browser. The goal is to eliminate that context switch entirely: capture, view, and manage the full task lifecycle without leaving the terminal.

The project skeleton already exists at `~/dev/knbn`. It is a Python package named `knbn`, built with `uv`, linted with `ruff`, type-checked with `mypy`, and tested with `pytest`. The current `src/knbn/__init__.py` and `src/knbn/__main__.py` are placeholder boilerplate — they will be replaced by the real implementation.

---

## 2. Data Model

### 2.1 Task Fields

Every task has exactly the following fields. The CSV column names are canonical (used in file headers and internal code).

| CSV Column | Internal Name | Type | Required | Notes |
|---|---|---|---|---|
| `Name` | `title` | `str` | Yes | Short task label, free text |
| `Category` | `category` | `str` (enum-like) | Yes | One of the configured category values; see §2.3 |
| `Status` | `status` | `str` (enum) | Yes | One of the configured status values; see §2.4 |
| `Priority` | `priority` | `str` (enum) | Yes | One of the configured priority values; see §2.2 |
| `DateTimeDue` | `due` | `str` (datetime, optional) | No | Format: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`; empty when absent |
| `KeyResource` | `key_resource` | `str` (URL, optional) | No | Single URL; empty string when absent |
| `FreeText1` | `free_text_1` | `str` (optional) | No | User-configurable free text field; label set in board config (default: `Feedback From`) |
| `FreeText2` | `free_text_2` | `str` (optional) | No | User-configurable free text field; label set in board config (default: `Delegated To`) |
| `FreeText3` | `free_text_3` | `str` (optional) | No | User-configurable free text field; label set in board config (empty by default) |
| `DateTimeCreated` | `date_created` | `str` (datetime) | Yes | Format: `YYYY-MM-DD HH:MM`; set automatically on creation; never edited |
| `DateTimeEdited` | `date_modified` | `str` (datetime) | Yes | Same format; updated automatically on every save |

**Derived / display-only field** (not stored in CSV):
- `notes_file` — presence of a corresponding Markdown file; see §3.2.

### 2.2 Priority Values

Exactly three values, in this rank order (highest first):

1. `High`
2. `Medium`
3. `Low`

### 2.3 Category Values

Categories are configured in `settings.json` under `board.categories`. Each entry has a `name` and a `color` (hex string). The default set is:

- `People`
- `Strategy`
- `Product`
- `Engineering`
- `Other`

Categories are free-form strings — no fixed enum enforcement at the data layer. The UI presents known values as suggestions. New categories can be added via the setup wizard or by editing `settings.json` directly.

### 2.4 Status Values and Task Lifecycle

Statuses are configured in `settings.json` under `board.active_statuses` and `board.terminal_statuses`. The defaults are:

**Active statuses** (shown on the Kanban board):

| Status | Meaning |
|---|---|
| `Todo` | Inbox / brain dump; not yet scheduled |
| `Now` | Active today / being worked on |
| `Feedback` | Blocked on input from another person |

**Terminal statuses** (archived; not shown on the live board):

| Status | Meaning |
|---|---|
| `Done` | Completed |
| `Delegated` | Handed off to someone else |
| `Stopped` | Deliberately abandoned |

**State machine** — allowed transitions (any direction is permitted; there is no enforced linear flow):

```
Todo  <-->  Now  <-->  Feedback
  \           |           /
   \----------|----------/
              v
        Done / Delegated / Stopped
```

In practice: any active status can transition to any other active status or to any terminal status. Terminal statuses do not transition back to active in the MVP (archiving is one-way).

### 2.5 Task Identity

Each task is identified by its position/row in the CSV. There is no UUID in the MVP. The CSV is the source of truth; ordering within a status+priority group follows insertion order (last created = bottom). This keeps the implementation simple and avoids auto-increment logic.

---

## 3. Storage Layer

### 3.1 Data Directory

On first launch, if no data directory exists, `knbn` initializes one at a configurable path (default: `~/.knbn/`). The directory contains:

```
~/.knbn/
  tasks.csv          # The task database
  notes/             # Per-task Markdown files (optional)
    <slug>.md
    <slug>.md
    ...
```

The data directory path is configurable via an environment variable `KNBN_DATA_DIR`. If the variable is set, that path is used instead of `~/.knbn/`.

### 3.2 CSV Schema

`tasks.csv` is a standard comma-separated file with a header row. Column order must match exactly:

```
DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,FreeText1,FreeText2,FreeText3,KeyResource
```

Rules:
- UTF-8 encoding (BOM-tolerant on read), Unix line endings (`\n`).
- Fields containing commas or newlines are quoted with double quotes per RFC 4180.
- Empty optional fields are represented as empty string (no value between consecutive commas).
- Dates are stored in `YYYY-MM-DD HH:MM` format (datetime) or `YYYY-MM-DD` (date-only).
- On load, the schema is validated; a mismatch raises a `ValueError` with a descriptive message.

**Legacy format**: Tasks exported from earlier versions used Notion's `Month D, YYYY H:MM AM/PM` date format. The parser accepts both formats transparently, but new writes always use `YYYY-MM-DD HH:MM`.

### 3.3 Markdown Notes Files

Each task *may* have an associated Markdown file stored in `notes/`. The filename is a URL-safe slug derived from the task title (lowercase, spaces → hyphens, non-alphanumeric stripped, max 60 chars). If two tasks produce the same slug, append `-2`, `-3`, etc.

A notes file is created when the user explicitly opens/creates the note from within the board. The file is opened in the user's `$EDITOR` (default: `vim`). If `$EDITOR` is not set, fall back to `nano`.

The notes file is plain Markdown — no metadata frontmatter in the MVP. The UI displays a visual indicator on a task card when a notes file exists.

---

## 4. CLI Interface

### 4.1 Entry Point

The CLI entry point is registered in `pyproject.toml` as:

```toml
[project.scripts]
knbn = 'knbn.__main__:main'
```

The command name is `knbn` (current `pyproject.toml` uses `knbn_cli` — this must be changed to `knbn`).

### 4.2 Commands

`knbn` uses subcommands:

#### `knbn` (no subcommand) / `knbn board`
Launches the full interactive TUI Kanban board. Opens the board view (§5.1) by default.

#### `knbn add`
Quick task capture from the terminal without opening the full board. Presents a short interactive prompt sequence (same as the existing `notion_task.py` flow):

1. **Title** — free-text prompt; required
2. **Status** — numbered selection; default `Todo`
   - If `Feedback` is selected, prompt additionally for **Feedback From** (free text)
   - If `Delegated` is selected, prompt additionally for **Delegated To** (free text)
3. **Priority** — numbered selection; default `Medium`
4. **Category** — numbered selection with existing categories listed; typing a new value adds it; default `Ideas`
5. **Key Resource** — URL prompt; press Enter to skip; enter `-` to explicitly leave empty

After capture, print a confirmation line (`✓ Task added: <title>`) and exit. The task is appended to `tasks.csv` with `Date Created` and `Last edited time` set to the current local time.

**Flags for `knbn add`**:

| Flag | Effect |
|---|---|
| `--title TEXT` | Pre-fill title, skip title prompt |
| `--status-default` | Use `Todo`, skip status prompt |
| `--priority-default` | Use `Medium`, skip priority prompt |
| `--category-default` | Use `Ideas`, skip category prompt |
| `--no-resource` | Skip key resource prompt |
| `--fast` / `-f` | Equivalent to all four `--*-default` + `--no-resource` |

This enables the same shell aliases the user had previously:

```sh
alias t='knbn add'                   # full prompts
alias f='knbn add --fast'            # all defaults
alias r='knbn add --fast --title'    # pre-fill title, all defaults
```

#### `knbn init [PATH]`
Initializes a new data directory at `PATH` (default: `~/.knbn/`). Creates the directory, an empty `tasks.csv` with the correct header, and a `notes/` subdirectory. Prints path on success. No-op if already initialized (prints existing path). Sets `KNBN_DATA_DIR` in the shell profile if `--setup-shell` flag is passed (MVP: omit this flag, just print instructions).

---

## 5. TUI Views

The TUI is implemented using the **Textual** library (Python). Textual provides a reactive widget system, keyboard handling, and terminal resize events — the best fit for this project's requirements.

Add `textual` to `[project.dependencies]` in `pyproject.toml`.

### 5.1 Kanban View (Primary View)

The board is a **config-driven matrix** of task cards. By default it has 3 columns × 3 rows.

**Columns** (left to right): configured `active_statuses` (default: `Todo` | `Now` | `Feedback`)
**Rows** (top to bottom): configured `priorities` (default: `High` | `Medium` | `Low`)

Each cell shows the tasks for that (status, priority) combination, stacked vertically. Each task is a card showing:
- Title (truncated to fit card width), with indicators appended: `☰` if a notes file exists, `※` if a key resource URL is set
- Due date (if set; shown right-aligned on the title line; dim when upcoming, bold red when overdue)
- Category tag (colored pill on the second line)

A thick amber right border on the card signals an upcoming deadline within the configured `deadline_warning_hours` window (default: 24 hours).

The board occupies the full terminal width and height. Column widths are equal (`floor(available_width / 3)`). Row heights distribute the remaining vertical space equally.

**Column headers** show the status name and count of tasks in that column:
```
 Todo  4          Now  3          Feedback  3
```

**Row headers** (swim lane labels) show the priority name on the left edge:
```
▼ High
▼ Medium
▼ Low
```

Swim lanes are collapsible (toggle with Enter or Space when the lane header is focused). Collapsed lanes show only the header with the task count.

**Minimum terminal size**: 100 columns × 30 rows. If the terminal is smaller, display an error message: `Terminal too small. Minimum size: 100×30.` and exit gracefully.

**Archive counts** are displayed in a bar below the board (above the footer), showing counts for each terminal status:
```
  Done    1302   Delegated    31   Stopped   112
```

### 5.2 Tabular View

A flat table listing all active tasks (Todo + Now + Feedback), grouped by Status. Within each status group, tasks are sorted by priority (High → Medium → Low), then by `Last edited time` descending.

Columns displayed: `Name` | `Status` | `Priority` | `Category` | `Created` | `Edited` | `Due Date`

The `Name` column is responsive — it takes all remaining space after the fixed-width columns are sized. Minimum title column width: 20 characters.

Group headers show status name and count:
```
▼ Now  3
  Research structured feedback models  High     Ideas
  Follow up on roadmap review session  Medium   Work Life
  Schedule engineering all-hands       Medium   Product

▼ Feedback  3
  ...
```

### 5.3 Closed View

Shows terminal-status tasks (Done + Delegated + Stopped, or whatever `terminal_statuses` are configured) grouped by ISO calendar week of `date_modified`, most recent week first.

Group header format: `Jul 12–18 2026  7` (date range + count)

Columns: `Name` | `Status` | `Priority` | `Category` | `Created` | `Edited` | `Due Date`

### 5.4 View Switching

Views are accessible via keyboard shortcuts and displayed in a top navigation bar:

| Key | View |
|---|---|
| `1` | Kanban (default) |
| `2` | Tabular |
| `3` | Closed |

The top bar also shows the active view name and the data directory path.

---

## 6. Keyboard Navigation and Interactions

All interactions are keyboard-driven. Mouse support is not required in the MVP.

### 6.1 Global Keys (all views)

| Key | Action |
|---|---|
| `q` / `Ctrl+C` | Quit application |
| `1` | Switch to Kanban view |
| `2` | Switch to Tabular view |
| `3` | Switch to Closed view |
| `a` | Open quick-add form (inline, without leaving the TUI) |
| `?` | Show key bindings help overlay |

### 6.2 Kanban View Navigation

| Key | Action |
|---|---|
| `←` / `→` | Move focus between columns |
| `↑` / `↓` | Move focus between items within a column (cards and lane headers) |
| `Shift+←` / `Shift+→` | Move focused task to the previous/next status column |
| `Enter` / `e` | Edit task (opens inline edit form) |
| `n` | Open / create Markdown notes for focused task |
| `o` | Open Key Resource URL in default browser (`open <url>` on macOS) |
| `d` | Move focused task to the configured default terminal status (default: `Done`) |
| `Del` / `Backspace` | Confirm-delete focused task (shows confirmation prompt) |
| `PgUp` | Promote task: move up within its lane; at the top, promotes to the next higher priority |
| `PgDn` | Demote task: move down within its lane; at the bottom, demotes to the next lower priority |
| `Enter` on lane header | Collapse/expand swim lane |

### 6.3 Inline Add / Edit Form

The quick-add form opens as an overlay modal. Fields are navigated with `Tab`/`Shift+Tab`. `Enter` on the last field (or a Submit button) saves. `Esc` cancels without saving.

Form fields (in order): Title → Status → Priority → Category → Due Date → Key Resource → Feedback From (conditional) → Delegated To (conditional).

"Conditional" fields only appear when the relevant status is selected.

---

## 7. Task Card Rendering

### 7.1 Card Layout

Two-line layout. Line 1: title with optional indicators and due date. Line 2: category tag.

```
┌─────────────────────────────┐
│ Research feedback models    │
│ [Ideas]                     │
└─────────────────────────────┘
```

With a due date:
```
┌─────────────────────────────┐
│ Org planning with SLT  2026-07-17│
│ [People]                    │
└─────────────────────────────┘
```

**Indicators** appended to the title (before the due date padding):
- `☰` — a Markdown notes file exists
- `※` — a key resource URL is set
- Both: `☰ ※`

**Due date styling**: dim when upcoming; bold red when overdue (due < now).

**Deadline warning**: a thick amber right border is shown when due date is within `deadline_warning_hours` (default: 24h).

If the title is too long to fit, it is truncated with `…`.

### 7.2 Category Tag Colors

Category tag colors are configured in `settings.json` under `board.categories`. Each entry specifies a `name` and a `color` (6-digit lowercase hex, e.g. `#e879a0`). Unknown categories fall back to `#888888`.

Default color mapping:

| Category | Hex color |
|---|---|
| People | `#e879a0` |
| Strategy | `#7ec8e3` |
| Product | `#5b9bd5` |
| Engineering | `#4dbfbf` |
| Other | `#cccccc` |
| (unknown) | `#888888` |

### 7.3 Focused Card Highlight

The currently focused card gets a border highlight (e.g. bright white or blue border). Unfocused cards have a dim border.

---

## 8. Application Architecture

### 8.1 Module Structure

```
src/knbn/
  __init__.py          # Public API (empty)
  __main__.py          # CLI entry point; dispatches to subcommands
  cli.py               # Click command definitions (add, board, init)
  app.py               # Textual App class; top-level TUI wiring
  config.py            # resolve_data_dir(), settings.json load/save, BoardConfig
  setup.py             # First-run setup wizard (CLI prompts)
  defaults/
    settings.json      # Bundled factory-default board config and app settings
  model/
    task.py            # Task dataclass, parse_datetime, display_date, now_str
    store.py           # CSV read/write (atomic via .tmp rename), notes management
    slug.py            # Title → filename slug, collision suffixes
  views/
    _columns.py        # Shared column layout constants and format helpers
    _row.py            # TaskRow — focusable widget used in list views
    _row_list.py       # RowListView — base class for tabular/closed views
    kanban.py          # KanbanView (config-driven board)
    tabular.py         # TabularView (active tasks grouped by status)
    done_week.py       # ClosedView (terminal tasks grouped by ISO week)
  widgets/
    _confirm.py        # ConfirmDialog modal
    card.py            # TaskCard widget
    date_picker.py     # Date picker widget used in TaskForm
    form.py            # TaskForm modal
    help.py            # HelpOverlay modal
```

### 8.2 Task Dataclass

```python
@dataclass
class Task:
    title: str
    category: str
    status: str  # one of active_statuses or terminal_statuses
    priority: str  # one of priorities
    date_created: str  # stored as YYYY-MM-DD HH:MM
    date_modified: str  # stored as YYYY-MM-DD HH:MM
    due: str = ''
    key_resource: str = ''
    free_text_1: str = ''
    free_text_2: str = ''
    free_text_3: str = ''
```

### 8.3 Store Interface

The `store.py` module exposes:

```python
def load_tasks(data_dir: Path) -> list[Task]: ...
def save_tasks(data_dir: Path, tasks: list[Task]) -> None: ...
def add_task(data_dir: Path, task: Task) -> None: ...
def update_task(data_dir: Path, index: int, task: Task) -> None: ...
def delete_task(data_dir: Path, index: int) -> None: ...


def get_notes_path(data_dir: Path, task: Task) -> Path: ...
def notes_exist(data_dir: Path, task: Task) -> bool: ...
```

`save_tasks` writes the full CSV atomically (write to `.tasks.csv.tmp`, then rename). This prevents corruption on crash.

### 8.4 Date Handling

**Storage format** (new): `%Y-%m-%d %H:%M` for datetime fields (e.g. `2026-07-01 14:27`); `%Y-%m-%d` for date-only values.

**Legacy format** (read-only, for backward compatibility): `%B %d, %Y %I:%M %p` (e.g. `July 01, 2026 02:27 PM`). The parser accepts both transparently; new writes always use the new format.

`now_str()` returns `datetime.now().strftime('%Y-%m-%d %H:%M')`.

For display, `display_date(s)` normalises any supported format to `YYYY-MM-DD HH:MM` (with time) or `YYYY-MM-DD` (date-only). For overdue detection, `parse_datetime(s)` returns `(datetime, has_time) | None`.

---

## 9. Dependencies

Add to `[project.dependencies]` in `pyproject.toml`:

```toml
dependencies = [
    "textual>=0.80.0",
    "click>=8.1.0",
]
```

`click` handles the CLI layer (matching the existing `notion_task.py` pattern). `textual` handles the TUI.

No other runtime dependencies. Keep the dependency surface minimal.

---

## 10. Configuration

Configuration is stored in `settings.json` inside the data directory (default: `~/.knbn/settings.json`). It is created automatically on first run from bundled defaults (`src/knbn/defaults/settings.json`).

| Mechanism | Purpose |
|---|---|
| `KNBN_DATA_DIR` env var | Override default data directory (`~/.knbn/`) |
| `$EDITOR` env var | Editor used to open Markdown notes |
| `settings.json` → `app.theme` | Textual theme name (default: `catppuccin-frappe`) |
| `settings.json` → `app.deadline_warning_hours` | Hours before due date to show amber border warning (default: `24`) |
| `settings.json` → `board.*` | Full board config: statuses, priorities, categories, free text field labels |

### Board config structure (`board` block)

```json
{
  "active_statuses": ["Todo", "Now", "Feedback"],
  "default_active_status": "Todo",
  "terminal_statuses": ["Done", "Delegated", "Stopped"],
  "default_terminal_status": "Done",
  "priorities": ["High", "Medium", "Low"],
  "categories": [
    { "name": "People", "color": "#e879a0" }
  ],
  "free_text_fields": ["Feedback From", "Delegated To", ""]
}
```

Constraints: `active_statuses` 2–5 entries; `terminal_statuses` 1–3; `priorities` 1–5; `categories` 1–10; each name 2–20 characters; colors must match `#[0-9a-f]{6}`. A `BoardConfigError` is raised on invalid config at startup.

---

## 11. Testing Requirements

The project enforces `--cov-fail-under=95` in pytest configuration. Coverage excludes `__main__.py` (already configured).

### 11.1 What to Test

- `model/task.py` — dataclass construction, field validation edge cases
- `model/store.py` — CSV round-trip (load → modify → save → reload produces identical tasks), slug collision handling, notes file existence detection
- `model/slug.py` — slug generation: spaces, special characters, long titles, collision suffixes
- `cli.py` — `knbn add` with all flag combinations (mock `store.add_task`)
- `config.py` — env var override, default path fallback

### 11.2 What Not to Test in Unit Tests

TUI widget behavior (Textual widgets) is not unit-tested in the MVP. Integration/visual testing of the TUI is deferred. The `app.py`, `views/`, and `widgets/` modules are excluded from coverage requirements via `omit` config additions.

Add to `pyproject.toml`:
```toml
[tool.coverage.run]
omit = [
    "*/__main__.py",
    "*/app.py",
    "*/views/*",
    "*/widgets/*",
]
```

---

## 12. Code Quality Constraints

The existing `pyproject.toml` tooling applies:

- **ruff** — linting + formatting; all rules listed in `[tool.ruff.lint]` must pass
- **mypy** — strict typing; `disallow_untyped_defs = true`; all public functions must have type annotations
- **pre-commit** — hooks run on commit (`.pre-commit-config.yaml`)

Additional constraints:
- No `print()` calls in non-`__main__` modules (enforced by `T20` ruff rule). Use Textual's logging for debug output.
- All modules must be importable without side effects.
- No global mutable state. The `store` module is stateless — callers pass `data_dir`.

---

## 13. MVP Scope — Explicit Boundaries

### In Scope

- Full CRUD on tasks via the TUI (add, view, edit, archive/delete)
- Three views: Kanban, Tabular, Done-by-Week
- Markdown notes per task (create/edit via `$EDITOR`)
- Quick-add CLI (`knbn add`) with all existing flags
- Data persistence via CSV + notes folder
- Keyboard navigation throughout
- Overdue date highlighting
- Responsive layout with minimum size enforcement
- Category tag colors

### Out of Scope (MVP)

- Mouse support
- Multi-select / bulk operations
- Search / filter within views
- Sorting customization
- Import/export beyond Notion CSV compatibility
- Shell profile auto-configuration (`--setup-shell`)
- Sync to Notion or any external service
- Cross-platform compatibility (Windows) — macOS terminal only
- Themes / color customization
- Task ordering via drag (keyboard reorder within a lane is acceptable if trivial, otherwise deferred)
- Due date time picker (type free text)
- Recurring tasks

---

## 14. Shell Integration

The user's intended shell aliases (to be documented in README, not auto-configured):

```sh
# Full interactive add
alias t='knbn add'

# Fast add with all defaults (no prompts)
alias f='knbn add --fast'

# Fast add with pre-filled title (e.g.: f "my task title")
# Usage: r "Read this article later"
function r() { knbn add --fast --title "$*"; }
```

---

## 15. Initialization Flow

On every `knbn board` or `knbn add` invocation:

1. Resolve data directory: `KNBN_DATA_DIR` env var → `~/.knbn/`
2. If directory does not exist: print `Initializing knbn data at <path>...`, call `knbn init` logic, continue
3. If `tasks.csv` does not exist: create it with header row only
4. If `notes/` does not exist: create it
5. Load tasks from CSV and proceed

---

## 16. Reference: Source Data Sample

The file `tests/fixtures/tasks.csv` contains 16 generic tasks covering all six statuses and three priorities. It is the canonical test fixture for CSV parsing. An implementation that reads this file correctly and renders it on the Kanban board is the primary acceptance test for the MVP.

Expected active tasks on board (as of the fixture):
- **Now, High**: Research structured feedback models (Ideas)
- **Now, Medium**: Follow up on roadmap review session (Work Life)
- **Feedback, High**: Sync on headcount planning (People)
- **Todo, Medium**: Schedule engineering all-hands (Product)
- **Todo, Medium**: Write self assessment (People)

---

## 17. Project Files to Change / Create

| File | Action | Notes |
|---|---|---|
| `pyproject.toml` | Modify | Change entry point from `knbn_cli` to `knbn`; add `textual`, `click` dependencies; update coverage omit list |
| `src/knbn/__init__.py` | Replace | Remove `greet()` boilerplate |
| `src/knbn/__main__.py` | Replace | Wire `click` group; dispatch to `cli.py` |
| `src/knbn/cli.py` | Create | `knbn add`, `knbn board`, `knbn init` commands |
| `src/knbn/app.py` | Create | Textual `App` subclass |
| `src/knbn/views/kanban.py` | Create | |
| `src/knbn/views/tabular.py` | Create | |
| `src/knbn/views/done_week.py` | Create | |
| `src/knbn/widgets/card.py` | Create | |
| `src/knbn/widgets/form.py` | Create | Add/edit form overlay |
| `src/knbn/widgets/help.py` | Create | |
| `src/knbn/model/task.py` | Create | |
| `src/knbn/model/store.py` | Create | |
| `src/knbn/model/slug.py` | Create | |
| `src/knbn/config.py` | Create | |
| `tests/test_code.py` | Replace | Remove boilerplate; add real tests |
| `tests/test_store.py` | Create | |
| `tests/test_slug.py` | Create | |
| `tests/test_cli.py` | Create | |
| `tests/fixtures/tasks.csv` | Create | Copy of `_temp_/example-database-content.csv` |
