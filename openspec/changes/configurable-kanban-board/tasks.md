## 1. BoardConfig foundation

- [ ] 1.1 Add `CategoryConfig` dataclass (`name: str`, `color: str`) and `BoardConfig` dataclass with all fields to `config.py`
- [ ] 1.2 Add `BoardConfigError` exception class to `config.py`
- [ ] 1.3 Define 10-color auto-assignment palette and `BOARD_CONFIG_DEFAULTS` constant (legacy-compatible defaults) in `config.py`
- [ ] 1.4 Implement `load_board_config(data_dir) -> BoardConfig` with full constraint validation (raises `BoardConfigError` on violation)
- [ ] 1.5 Restructure `settings.json` schema: move `theme` and `deadline_warning_hours` under an `app` key; update `SETTINGS_DEFAULTS` to `{"app": {...}, "board": {...}}` shape
- [ ] 1.6 Replace `get_setting` / `get_int_setting` with `get_app_setting(key, default)`; update all callers (`app.py` theme watcher, `card.py` deadline hours)
- [ ] 1.7 Update `load_settings`/`save_settings` signatures from `dict[str, str]` to `dict[str, Any]`
- [ ] 1.8 Add `load_board_config(data_dir) -> BoardConfig` with full constraint validation (raises `BoardConfigError` on violation)
- [ ] 1.9 Add `BoardConfig` helper methods: `category_color(name)`, `active_free_text_fields()`, `all_statuses()`
- [ ] 1.10 Write unit tests for `load_board_config`: valid config, missing `board` key, absent file, each validation violation, helper methods; update existing settings tests for new `app` key structure

## 2. Task dataclass and CSV schema

- [ ] 2.1 Replace `feedback_from` and `delegated_to` fields on `Task` with `free_text_1`, `free_text_2`, `free_text_3` (all `str`, default `''`)
- [ ] 2.2 Remove `STATUS_ACTIVE`, `STATUS_TERMINAL`, `STATUS_VALUES`, `PRIORITY_VALUES`, `DEFAULT_CATEGORIES` constants from `task.py`
- [ ] 2.3 Update `_CSV_FIELDNAMES` in `store.py` to use `FreeText1`, `FreeText2`, `FreeText3` in place of `Delegate` and `Feedback`
- [ ] 2.4 Update `_row_to_task` and `_task_to_row` in `store.py` for the new field names
- [ ] 2.5 Update `tests/fixtures/tasks.csv` to use new CSV column names

## 3. Board setup wizard

- [ ] 3.1 Implement `run_setup_wizard(data_dir)` in `cli.py` (or a new `setup.py` module): interactive prompts for active statuses, terminal statuses, priorities, categories, free-text field labels with validation and re-prompts
- [ ] 3.2 Auto-assign category colors from palette in wizard output
- [ ] 3.3 Add wizard trigger check in `ensure_data_dir` (or at the start of `board`/`init` commands): skip if `tasks.csv` exists or `board` key present in `settings.json`
- [ ] 3.4 Ensure `knbn init` runs wizard then exits; ensure `knbn board` runs wizard then launches TUI
- [ ] 3.5 Write unit tests for wizard trigger logic (blank slate → wizard, tasks exist → skip, board config exists → skip)

## 4. Wire BoardConfig through the TUI

- [ ] 4.1 Load `BoardConfig` once at startup in `KnbnApp.on_mount` (or `__init__`) and store as `self.board_config`; handle `BoardConfigError` with a user-facing error screen and graceful exit
- [ ] 4.2 Pass `board_config` to `KanbanView` and `TabularView` on construction (or expose via `self.app.board_config` accessor)

## 5. Kanban view: config-driven layout and actions

- [ ] 5.1 Replace hardcoded `_STATUS_ORDER` in `kanban.py` with `board_config.active_statuses` (leftmost = `default_active_status`)
- [ ] 5.2 Replace `PRIORITY_VALUES` swim-lane iteration with `board_config.priorities`
- [ ] 5.3 Replace `CATEGORY_COLORS` dict import in `card.py` with `board_config.category_color(name)` calls
- [ ] 5.4 Update `action_move_up` / `action_move_down` to use `board_config.priorities.index(...)` for promote/demote logic
- [ ] 5.5 Update footer rendering in kanban view to iterate `board_config.terminal_statuses` for archive counts
- [ ] 5.6 Update `action_mark_done` to use `board_config.default_terminal_status` (label and status value)
- [ ] 5.7 Remove `action_mark_stopped`, `action_mark_delegated`, their keybindings (`x`, `g`), and all `ConfirmDialog`/`PromptModal` code they used
- [ ] 5.8 Update `done_week.py` filter to use `board_config.terminal_statuses` instead of the removed `STATUS_TERMINAL` constant

## 6. Form and detail widgets

- [ ] 6.1 Update `form.py` Status `Select` to populate from `board_config.all_statuses()`
- [ ] 6.2 Update `form.py` Priority `Select` to populate from `board_config.priorities`
- [ ] 6.3 Update `form.py` Category `Select` to populate from `[c.name for c in board_config.categories]`
- [ ] 6.4 Replace the static `Feedback From` / `Delegated To` `Input` widgets in `form.py` with dynamically rendered inputs based on `board_config.active_free_text_fields()`; wire save/load to `free_text_1`/`free_text_2`/`free_text_3`
- [ ] 6.5 Update `detail.py` to display free-text fields using labels from `board_config` (only non-empty slots, only when value is non-empty)

## 7. CLI updates

- [ ] 7.1 Update `cli.py add` status prompt to use `board_config.active_statuses` (remove hardcoded `STATUS_ACTIVE + ['Delegated']`)
- [ ] 7.2 Update `cli.py add` priority prompt to use `board_config.priorities`
- [ ] 7.3 Update `cli.py add` category prompt to use `[c.name for c in board_config.categories]`
- [ ] 7.4 Remove the `delegated_to` conditional prompt (status == 'Delegated') from `cli.py add`; prompt for configured free-text fields generically if desired (or omit — TUI form handles them)

## 8. Help overlay and keybinding cleanup

- [ ] 8.1 Remove `x — Mark Stopped` and `g — Mark Delegated` entries from `help.py`
- [ ] 8.2 Update `d — Mark Done` help text to reflect "Mark <default_terminal_status>"

## 9. Test suite updates

- [ ] 9.1 Replace all remaining `STATUS_ACTIVE`, `STATUS_TERMINAL`, `STATUS_VALUES`, `PRIORITY_VALUES`, `DEFAULT_CATEGORIES` references in tests with a shared `default_board_config()` test fixture
- [ ] 9.2 Verify full test suite passes with `uv run pytest tests` and coverage floor holds
- [ ] 9.3 Run `make build` (test + mypy + lint + format) clean
