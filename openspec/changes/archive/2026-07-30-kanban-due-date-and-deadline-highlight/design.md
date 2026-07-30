## Context

Task cards currently render a two-row layout: title row (with indicators) and a bottom row with the category tag and optionally an overdue date in `DD/MM/YYYY` format. The due-date parser (`_parse_due`) uses `DD/MM/YYYY` format, which is inconsistent with the canonical `YYYY-MM-DD` / `YYYY-MM-DD HH:MM` formats used everywhere else in the app. The warning highlight for overdue tasks exists (red bold text) but there is no lookahead warning for tasks approaching their deadline.

## Goals / Non-Goals

**Goals:**
- Show due date right-aligned on the title row of a card (when set)
- Apply a CSS warning class to cards whose due date is within `deadline_warning_hours` hours of now (or already past)
- Add `deadline_warning_hours` to `SETTINGS_DEFAULTS` with a default of `24`
- Fix `_parse_due` in `card.py` to use `parse_datetime` from `task.py` (canonical parser, handles both `YYYY-MM-DD` and `YYYY-MM-DD HH:MM`)

**Non-Goals:**
- Changing the due date format stored in the CSV
- Adding a due-date filter or sort to any view
- Modifying the tabular or closed views

## Decisions

**Due date placement: right-aligned on title row**

The title row currently holds the truncated title + indicator glyphs (`☰ ※`). Appending the due date right-aligned (padded with spaces to fill the card width) keeps it visible without adding a third row. The title is truncated further to leave space for the date string when a due date is present.

Alternative considered: third row below the category tag. Rejected — adds height to every card that has a due date, which is visually noisy and wastes vertical space.

**Highlighting: CSS reactive class on TaskCard**

Textual supports `add_class` / `remove_class` on widgets. Adding a `.-deadline-warning` class to `TaskCard` when the deadline is within the threshold lets CSS control the visual: a yellow/amber border (`$warning`). This is the standard Textual pattern and keeps rendering logic out of Python business logic.

The class is set in `on_mount` and updated on `on_resize` (which already triggers recompose) — no timer needed since the board refreshes on every task mutation. For a long-running session the class will be set correctly on the next board reload.

**`deadline_warning_hours` storage: string in settings**

`SETTINGS_DEFAULTS` values are strings (consistent with the existing `theme` key and `load_settings` which casts all values to `str`). The card widget reads the value via `get_setting` and converts to `int`, defaulting to `24` on parse error.

**Parser fix: use canonical `parse_datetime`**

`_parse_due` currently calls `datetime.strptime(date_part, '%d/%m/%Y')` — this was left over from Notion's export format and never matched the canonical format. Switching to `parse_datetime` from `task.py` corrects this with no data migration needed (the CSV already stores dates in `YYYY-MM-DD` / `YYYY-MM-DD HH:MM`).

## Risks / Trade-offs

- [Card height] Adding the due date to the title row does not change card height. If the title is very long, it will be truncated more aggressively to fit both title and date. → Acceptable trade-off; the truncation logic already handles this.
- [Warning staleness] The warning class is set at render time and not updated on a live timer. A card that crosses the threshold during a session will only update on the next board recompose. → Acceptable for a personal kanban tool; the user can press `r` or switch views to force a reload.
- [Settings type] `deadline_warning_hours` is stored as a string. A non-numeric value in `settings.json` silently falls back to 24. → Document in the spec; consistent with existing settings behaviour.
