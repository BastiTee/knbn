## Why

`knbn` is currently hardwired to one specific workflow: three active statuses, two terminal statuses plus Stopped, three priorities, seven fixed categories, and two fixed free-text fields ("Feedback From" / "Delegated To"). Any other user wanting to adopt the tool must patch the source. Moving this configuration into `settings.json` — with a guided setup wizard on first launch — makes knbn genuinely reusable beyond the author's workflow.

## What Changes

- **New**: `settings.json` gains a board-config block defining statuses (2–5 active, 1–3 terminal with one default each), priorities (1–5), categories (1–10 with auto-assigned colors), and free-text fields (0–3 user-named fields).
- **New**: First-run setup wizard walks the user through the board-config questions when `knbn board` or `knbn init` is called on an empty data directory.
- **BREAKING**: CSV schema changes — the two fixed free-text columns (`Delegate`, `Feedback`) are replaced by up to three generic columns (`FreeText1`, `FreeText2`, `FreeText3`); display labels come from `settings.json`. Existing task data requires a one-time migration.
- **Remove**: `action_mark_stopped` (key `x`) and `action_mark_delegated` (key `g`) quick-action shortcuts and their `ConfirmDialog`/`PromptModal` flows in `kanban.py`. Users set terminal states via the edit form or a configurable "mark done" shortcut for the default terminal status only.
- **Change**: `STATUS_ACTIVE`, `STATUS_TERMINAL`, `PRIORITY_VALUES`, and `DEFAULT_CATEGORIES` in `task.py` and the `_STATUS_ORDER` duplication in `kanban.py` are replaced by config-loaded values at runtime.
- **Change**: Kanban board lane count and labels driven by configured active statuses; swim-lane count and labels driven by configured priorities; promote/demote actions (`↑`/`↓`) use config priority order.
- **Change**: Category color palette auto-assigned on setup; stored in `settings.json`; user-editable manually but no TUI for it.
- **Change**: CLI `add` command reads statuses, priorities, and categories from config rather than hardcoded constants.

## Capabilities

### New Capabilities

- `board-setup-wizard`: Interactive first-run CLI wizard that collects board configuration (statuses, default active/terminal status, priorities, categories, free-text field names) and writes them to `settings.json`.
- `board-config`: `settings.json` schema and loader for the configurable board fields — validation rules (min/max counts, required defaults), runtime access helpers, and auto-assigned category colors.

### Modified Capabilities

- `task-model`: Status and priority enumerations are no longer compile-time constants; they are loaded from board config at runtime. The `Task` dataclass free-text fields (`feedback_from`, `delegated_to`) are replaced by three generic fields (`free_text_1`, `free_text_2`, `free_text_3`) whose labels come from config.
- `app-settings`: `settings.json` schema is extended with the board-config block; `load_settings` / `save_settings` support nested structures (lists and dicts), not just `dict[str, str]`.
- `tui-board`: Board columns driven by configured active statuses; swim-lane rows driven by configured priorities; mark-stopped and mark-delegated quick actions removed; archive counts in footer reflect all configured terminal statuses.

## Impact

- `model/task.py` — `STATUS_ACTIVE`, `STATUS_TERMINAL`, `STATUS_VALUES`, `PRIORITY_VALUES`, `DEFAULT_CATEGORIES` constants removed or replaced; `Task` dataclass `feedback_from`/`delegated_to` fields replaced by `free_text_1`/`free_text_2`/`free_text_3`.
- `model/store.py` — CSV fieldnames list and strict schema validator must accommodate the new generic free-text columns; one-time migration function needed for existing data files.
- `config.py` — `settings.json` load/save upgraded to nested types; new board-config accessors (`get_active_statuses()`, `get_priorities()`, `get_categories()`, `get_free_text_fields()`, etc.).
- `views/kanban.py` — `_STATUS_ORDER` and swim-lane construction become config-driven; `action_mark_stopped` and `action_mark_delegated` removed; footer counts iterate configured terminal statuses.
- `widgets/card.py` — `CATEGORY_COLORS` dict loaded from `settings.json` instead of hardcoded.
- `widgets/form.py` — Status `Select` options, Priority `Select` options, Category `Select` options, and free-text `Input` labels all loaded from config.
- `cli.py` — Status and priority choices in `knbn add` read from config; `delegated_to` conditional prompt removed (no more special-cased statuses in CLI).
- No new Python dependencies required; all within existing stdlib + Textual + Click stack.
