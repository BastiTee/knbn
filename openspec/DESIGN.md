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
| `Category` | `category` | `str` (enum-like) | Yes | One of the predefined category values; see §2.3 |
| `Status` | `status` | `str` (enum) | Yes | One of the six status values; see §2.4 |
| `Priority` | `priority` | `str` (enum) | Yes | `High`, `Medium`, or `Low` |
| `Due` | `due` | `str` (datetime, optional) | No | Format: `DD/MM/YYYY HH:MM (GMT+N)` as used in source data; stored as-is, displayed as date only |
| `Key Resource` | `key_resource` | `str` (URL, optional) | No | Single URL; empty string when absent |
| `Feedback From` | `feedback_from` | `str` (optional) | No | Name of person; populated only for `Feedback` status tasks |
| `Delegated To` | `delegated_to` | `str` (optional) | No | Name of person; populated only for `Delegated` status tasks |
| `Date Created` | `date_created` | `str` (datetime) | Yes | Format: `Month D, YYYY H:MM AM/PM`; set automatically on creation; never edited |
| `Last edited time` | `date_modified` | `str` (datetime) | Yes | Same format; updated automatically on every save |

**Derived / display-only field** (not stored in CSV):
- `notes_file` — presence of a corresponding Markdown file; see §3.2.

### 2.2 Priority Values

Exactly three values, in this rank order (highest first):

1. `High`
2. `Medium`
3. `Low`

### 2.3 Category Values

The category list is drawn from the existing Notion database (screenshot of category picker). These are the predefined values; the implementation must allow the user to type a new value that is then added to the list:

- `People`
- `Hiring`
- `Strategy`
- `Product`
- `Engineering`
- `Work Life`
- `Ideas`

Categories are free-form strings — no fixed enum enforcement at the data layer. The UI presents known values as suggestions.

### 2.4 Status Values and Task Lifecycle

Six statuses, split into two groups:

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

`tasks.csv` is a standard comma-separated file with a header row. Column order must match exactly (for forward compatibility):

```
Name,Category,Date Created,Delegated To,Due,Feedback From,Key Resource,Last edited time,Priority,Status
```

This matches the existing Notion CSV export format. Importing a Notion CSV export (e.g. `_temp_/example-database-content.csv`) requires no transformation — the tool should be able to read it directly.

Rules:
- UTF-8 encoding, Unix line endings (`\n`).
- Fields containing commas or newlines are quoted with double quotes per RFC 4180.
- Empty optional fields are represented as empty string (no value between consecutive commas).
- Dates are stored as strings in the format present in the source data (`Month D, YYYY H:MM AM/PM`).

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

The board is a **3-column × 3-row matrix** of task cards.

**Columns** (left to right): `Todo` | `Now` | `Feedback`
**Rows** (top to bottom): `High` | `Medium` | `Low`

Each cell shows the tasks for that (status, priority) combination, stacked vertically. Each task is a card showing:
- Title (truncated to fit card width)
- Category tag (colored pill)
- Due date (if set; shown in a muted color; highlighted red if overdue)
- Notes indicator icon (e.g. `📝` or `[N]`) if a Markdown notes file exists

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

**Archive counts** are shown in a right-side sidebar (or status bar, whichever fits) showing Done/Delegated/Stopped counts, mirroring the Notion "Pinned groups" panel:
```
  Done      1302
  Delegated   31
  Stopped    112
```

### 5.2 Tabular View

A flat table listing all active tasks (Todo + Now + Feedback), grouped by Status. Within each status group, tasks are sorted by priority (High → Medium → Low), then by `Last edited time` descending.

Columns displayed: `Name` | `Priority` | `Category` | `Due`

Column widths: Name takes remaining space after other columns are sized. Priority and Category are fixed-width. Due is fixed-width.

Group headers show status name and count:
```
▼ Now  3
  Research structured feedback models  High     Ideas
  Follow up on roadmap review session  Medium   Work Life
  Schedule engineering all-hands       Medium   Product

▼ Feedback  3
  ...
```

### 5.3 Done-by-Week View

Shows archived tasks (Done + Delegated + Stopped) grouped by ISO calendar week of `Last edited time`, most recent week first.

Group header format: `Jul 12–18 2026  7` (date range + count)

Columns: `Name` | `Category` | `Priority` | `Last edited time` | `Date Created`

### 5.4 View Switching

Views are accessible via keyboard shortcuts and displayed in a top navigation bar:

| Key | View |
|---|---|
| `1` | Kanban (default) |
| `2` | Tabular |
| `3` | Done-by-Week |

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
| `3` | Switch to Done-by-Week view |
| `a` | Open quick-add form (inline, without leaving the TUI) |
| `r` | Reload data from CSV (manual refresh) |
| `?` | Show key bindings help overlay |

### 6.2 Kanban View Navigation

| Key | Action |
|---|---|
| `←` / `→` | Move focus between columns |
| `↑` / `↓` | Move focus between task cards within a column |
| `Tab` | Next card (wraps across columns/rows) |
| `Shift+Tab` | Previous card |
| `Enter` | Open task detail panel |
| `e` | Edit task (opens inline edit form) |
| `n` | Open / create Markdown notes for focused task |
| `d` | Move focused task to Done |
| `x` | Move focused task to Stopped |
| `g` | Delegate focused task (prompts for Delegated To name) |
| `m` | Move focused task (prompts for new status selection) |
| `p` | Change priority of focused task |
| `Del` / `Backspace` | Confirm-delete focused task (shows confirmation prompt) |
| `Space` / `Enter` on lane header | Collapse/expand swim lane |

### 6.3 Task Detail Panel

Triggered by `Enter` on a focused card. Opens a right-side panel (or overlay) showing all task fields. Navigation within panel:

| Key | Action |
|---|---|
| `Esc` / `q` | Close panel, return to board |
| `e` | Edit task |
| `n` | Open notes in `$EDITOR` |
| `o` | Open Key Resource URL in default browser (`open <url>` on macOS) |

### 6.4 Inline Add / Edit Form

The quick-add form opens as an overlay modal. Fields are navigated with `Tab`/`Shift+Tab`. `Enter` on the last field (or a Submit button) saves. `Esc` cancels without saving.

Form fields (in order): Title → Status → Priority → Category → Due Date → Key Resource → Feedback From (conditional) → Delegated To (conditional).

"Conditional" fields only appear when the relevant status is selected.

---

## 7. Task Card Rendering

### 7.1 Card Layout

```
┌─────────────────────────────┐
│ Research feedback models    │
│ [Ideas]          High       │
└─────────────────────────────┘
```

If a due date is set:
```
┌─────────────────────────────┐
│ Org planning with SLT       │
│ [People]        17/07/2026 ⏰│
└─────────────────────────────┘
```

If a notes file exists, append a `📝` (or plain `[N]` in environments without emoji support) after the title.

If overdue (due date < today), the due date is rendered in red/bold.

### 7.2 Category Tag Colors

Category tags use consistent colors. The color mapping is fixed and derived from the visual appearance in Notion screenshots:

| Category | Color |
|---|---|
| People | Pink / rose |
| Hiring | Light pink |
| Strategy | Light blue |
| Product | Blue |
| Engineering | Blue-green / teal |
| Work Life | Orange / yellow |
| Ideas | White / neutral |
| (unknown) | Gray |

In Textual, these map to named color constants or CSS color strings on the tag widget.

### 7.3 Focused Card Highlight

The currently focused card gets a border highlight (e.g. bright white or blue border). Unfocused cards have a dim border.

---

## 8. Application Architecture

### 8.1 Module Structure

```
src/knbn/
  __init__.py          # Public API (empty for now; no exported symbols needed)
  __main__.py          # CLI entry point; dispatches to subcommands
  cli.py               # Click command definitions (add, board, init)
  app.py               # Textual App class; top-level TUI wiring
  views/
    kanban.py          # KanbanView widget
    tabular.py         # TabularView widget
    done_week.py       # DoneByWeekView widget
  widgets/
    card.py            # TaskCard widget
    form.py            # Add/edit form overlay
    detail.py          # Task detail panel
    help.py            # Key bindings help overlay
  model/
    task.py            # Task dataclass + field validation
    store.py           # CSV read/write; Markdown notes management
    slug.py            # Title → filename slug utility
  config.py            # Data directory resolution (env var + default)
```

### 8.2 Task Dataclass

```python
@dataclass
class Task:
    title: str
    category: str
    status: str  # one of STATUS_VALUES
    priority: str  # one of PRIORITY_VALUES
    date_created: str  # stored as original string
    date_modified: str  # stored as original string
    due: str = ''
    key_resource: str = ''
    feedback_from: str = ''
    delegated_to: str = ''
```

Constants:
```python
STATUS_ACTIVE = ['Todo', 'Now', 'Feedback']
STATUS_TERMINAL = ['Done', 'Delegated', 'Stopped']
STATUS_VALUES = STATUS_ACTIVE + STATUS_TERMINAL
PRIORITY_VALUES = ['High', 'Medium', 'Low']
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

Dates are stored as strings matching the Notion CSV format. For comparison (overdue detection, week grouping), they are parsed on read using `datetime.strptime`. The exact format strings:

- `Date Created` / `Last edited time`: `"%B %d, %Y %I:%M %p"` (e.g. `July 1, 2026 2:27 PM`)
- `Due`: `"%d/%m/%Y %H:%M (%Z)"` — but since `GMT+2` is not a valid Python `%Z` token, parse only the date portion `"%d/%m/%Y"` for display and comparison purposes.

When `knbn` writes new dates (on task creation/modification), it uses: `datetime.now().strftime("%B %-d, %Y %-I:%M %p")` (macOS/Linux). This produces `July 1, 2026 2:27 PM`.

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

No configuration file in the MVP. All configuration is via:

| Mechanism | Purpose |
|---|---|
| `KNBN_DATA_DIR` env var | Override default data directory (`~/.knbn/`) |
| `$EDITOR` env var | Editor used to open Markdown notes |

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
| `src/knbn/widgets/form.py` | Create | |
| `src/knbn/widgets/detail.py` | Create | |
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
