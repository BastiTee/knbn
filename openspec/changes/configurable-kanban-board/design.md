## Context

`knbn` is a single-user terminal Kanban app whose statuses, priorities, categories, and free-text fields are currently hardcoded in Python constants and a rigid CSV schema. Three sets of hardcoded structures are scattered across the codebase (`STATUS_ACTIVE`/`STATUS_TERMINAL` in `task.py`, `_STATUS_ORDER` duplicated in `kanban.py`, `CATEGORY_COLORS` in `card.py`), making any configuration change require source edits. The existing `settings.json` infrastructure (atomic load/save, `~/.knbn/` data dir) gives a natural home for board configuration; the challenge is migrating the data model and wiring config through the whole stack without breaking existing data.

## Goals / Non-Goals

**Goals:**
- Let users define 2–5 active statuses, 1–3 terminal statuses, 1–5 priorities, 1–10 categories, and 0–3 free-text field labels via `settings.json`.
- Provide a guided CLI wizard for first-time setup in an empty data directory.
- Remove the `mark_stopped` (key `x`) and `mark_delegated` (key `g`) quick actions; keep `mark_done` (key `d`) as the single terminal shortcut targeting the configured default terminal status.

**Non-Goals:**
- A TUI settings editor — manual `settings.json` edits are the supported path for reconfiguration after setup.
- Multi-user or shared boards.
- Import/export between differently-configured boards.
- Category color picking in the wizard — colors are auto-assigned; manual override in `settings.json` is supported.
- Automatic migration of existing CSV data or `settings.json` — all installs are controlled by the author and will be updated manually during the apply phase.
- Board reconfiguration after initial setup — the `board` block in `settings.json` is write-once via the wizard; subsequent changes are manual edits at the user's own risk.

## Decisions

### D1 — `settings.json` has two top-level blocks: `app` and `board`

**Decision:** `settings.json` is structured with exactly two nested objects: `app` (holds `theme`, `deadline_warning_hours`, and any future application-level settings) and `board` (holds `active_statuses`, `default_active_status`, `terminal_statuses`, `default_terminal_status`, `priorities`, `categories`, and `free_text_fields`). There are no flat top-level keys.

**Alternatives considered:**
- Keep `theme`/`deadline_warning_hours` as flat top-level strings alongside `board` — rejected; mixing flat strings and nested dicts in the same file is inconsistent and makes the schema harder to reason about.
- Separate `app.json` and `board.json` — rejected; two config files for one tool is unnecessary.
- Environment variables — rejected; lists of values are unwieldy in env vars and don't persist across sessions.

**Consequences:** `load_settings`/`save_settings` must move from `dict[str, str]` to `dict[str, Any]`. All existing callers of `get_setting('theme')` and `get_int_setting('deadline_warning_hours')` must be updated to read from `settings['app']`. The new accessor is `get_app_setting(key, default)`.

---

### D2 — Free-text columns in CSV use generic names `FreeText1`/`FreeText2`/`FreeText3`

**Decision:** The CSV always has exactly three generic free-text columns (`FreeText1`, `FreeText2`, `FreeText3`), even if fewer than three are configured. Display labels come from `settings.json`. Empty columns are stored as empty strings.

**Alternatives considered:**
- Use configured label names as CSV column names — rejected; changing labels would break the CSV schema; the strict `_validate_csv_schema` check would reject existing files.
- Keep `Delegate`/`Feedback` columns — rejected; semantically wrong for boards that don't use delegation/feedback workflows.

**Consequences:** This is a **breaking CSV schema change**. Existing data files must be updated manually (see Migration Plan).

---

### D3 — `BoardConfig` dataclass loaded once at startup

**Decision:** Introduce a `BoardConfig` dataclass in `config.py` (or a new `model/board_config.py`) populated by `load_board_config()` reading from `settings.json`. The `KnbnApp` stores it as `self.board_config` and passes it to views/widgets that need it. The CLI `add` command calls `load_board_config()` directly.

**Alternatives considered:**
- Global module-level singleton — rejected; hard to test and creates import-order dependencies.
- Re-read settings.json on every access — rejected; repeated disk I/O for every status lookup is wasteful.

---

### D4 — Board configuration is a one-time, write-once process

**Decision:** The wizard runs exactly once — when both `tasks.csv` and the `board` key in `settings.json` are absent. Once the `board` block exists in `settings.json`, the wizard never runs again. There is no re-configuration command, no reset flow, and no in-app settings editor. Users who want to change their board setup must edit `settings.json` manually and handle any resulting data inconsistencies (e.g., tasks with a status that no longer exists in config) themselves.

**Rationale:** Reconfiguration after tasks exist is inherently risky — renamed statuses silently orphan existing task records. By making setup write-once and putting the burden of manual edits on the user, the system avoids complex migration logic and stays simple. Users who need a different config can start a fresh data directory.

---

### D5 — Category colors auto-assigned from a fixed 10-color palette

**Decision:** On wizard completion (or when defaults are synthesized), each category is assigned a color from a predefined palette cycling in order. Colors are stored in `settings.json` under each category entry. The user can change them manually. No TUI for color picking.

**Palette (10 colors):** Reuse the existing `CATEGORY_COLORS` values for the first seven; add three more for the up-to-10 slot.

---

### D6 — `mark_done` keeps key `d`; `mark_stopped`/`mark_delegated` removed

**Decision:** Key `d` transitions the focused task to `default_terminal_status` (set in board config). The Stopped and Delegated quick-action shortcuts (`x`, `g`) and their `ConfirmDialog`/`PromptModal` flows are removed entirely. Users who want other terminal statuses must use the edit form.

**Rationale:** These shortcuts were tied to specific hardcoded status names. In a configurable model, making every terminal status a shortcut is impractical; one shortcut for the most common archive action is sufficient.

---

### D7 — `Task` dataclass gains `free_text_1`, `free_text_2`, `free_text_3`

**Decision:** Replace `feedback_from` and `delegated_to` with three generic string fields `free_text_1`, `free_text_2`, `free_text_3`, all defaulting to `''`. The semantic meaning of each field is purely in the label stored in `settings.json`.

**Consequences:** All code that referenced `feedback_from` or `delegated_to` by field name must be updated. The `cli.py` conditional "prompt only if status is Delegated/Feedback" logic is removed.

## Risks / Trade-offs

**Risk: Invalid manual edits to `settings.json`** → Mitigation: `load_board_config()` validates all constraints (min/max counts, default exists in list) and raises `BoardConfigError` with a clear message; the app displays the error and exits rather than silently misbehaving.

**Risk: Tests reference removed constants** → Mitigation: All references to `STATUS_ACTIVE`, `STATUS_TERMINAL`, `PRIORITY_VALUES`, `DEFAULT_CATEGORIES` in tests must be replaced with a test `BoardConfig` fixture. Tracked as an implementation task.

**Risk: Hardcoded status names in third-party integrations or scripts** → Low risk for a personal tool; no external API. Documented as a breaking change in the change proposal.

**Trade-off: No reconfiguration wizard** — Once a board is set up, reconfiguration requires manual `settings.json` edits. Re-running the wizard on an existing board is not supported, to avoid accidentally overwriting live data. Users who want to reconfigure must edit the file and handle any data migration (e.g., status renaming in existing tasks) themselves.

## Migration Plan

All existing installs (personal and demo) are controlled by the author and will be updated manually during the apply phase:

1. Rename `Delegate` → `FreeText1` and `Feedback` → `FreeText2` in the CSV header; add empty `FreeText3` column.
2. Add the `board` config block to `settings.json` with values matching the current hardcoded defaults.

No automated migration code is shipped.

## Open Questions

- **Q1**: Should the wizard be re-enterable via a `knbn config` subcommand in the future? (Out of scope for this change; leaving as a placeholder.)
- **Q2**: The Kanban board currently enforces a minimum 3-column layout. With 2 active statuses, does the layout break? Implementation must handle 2–5 columns gracefully — minimum terminal width may need adjustment.
- **Q3**: The `done_week.py` view groups archived tasks by ISO week. With configurable terminal statuses, the filter must use all configured terminal statuses rather than the hardcoded `STATUS_TERMINAL` list. Confirm this is addressed in the tui-board spec.
