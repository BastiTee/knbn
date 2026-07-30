## Why

Task cards on the Kanban board show no due date at a glance, making it impossible to spot upcoming deadlines without opening each task. Users need a way to see due dates inline on cards and be warned when a deadline is imminent.

## What Changes

- Task cards display the due date right-aligned on the title row (when a due date is set)
- Cards approaching or past their deadline are visually highlighted with a warning border/style
- A new `deadline_warning_hours` setting (default: `24`) controls the lookahead window for the warning
- Fix the existing `_parse_due` helper in `card.py` to use the canonical `parse_datetime` from `task.py` (currently uses a broken legacy `DD/MM/YYYY` parser)

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `tui-board`: Task card rendering gains a right-aligned due date on the title row and a deadline-warning highlight; scenarios added for both behaviours
- `app-settings`: New `deadline_warning_hours` setting added with default value `24`

## Impact

- `src/knbn/widgets/card.py` — due date rendering, warning class, fix `_parse_due`
- `src/knbn/config.py` — add `deadline_warning_hours` to `SETTINGS_DEFAULTS`
- `openspec/specs/tui-board/spec.md` — updated card rendering requirement + scenarios
- `openspec/specs/app-settings/spec.md` — new requirement for `deadline_warning_hours`
