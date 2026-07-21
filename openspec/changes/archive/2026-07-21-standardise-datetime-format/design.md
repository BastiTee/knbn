## Context

Tasks store three date-bearing fields: `date_created`, `date_modified` (both written by `now_str()`), and `due` (typed by the user). Currently `now_str()` produces `"July 21, 2026 03:45 PM"` — verbose, locale-sensitive, and not lexicographically sortable. The `due` field accepts an inconsistent `DD/MM/YYYY HH:MM (TZ)` format (as seen in the fixture) with no validation. The table views use `_date_only()` which simply takes the first three whitespace-tokens, breaking silently on any unexpected format.

New canonical formats:
- **Date-only stored value**: `YYYY-MM-DD` (e.g. `2026-07-21`)
- **Datetime stored value**: `YYYY-MM-DD HH:MM` (e.g. `2026-07-21 15:45`)
- **Display**: show `YYYY-MM-DD HH:MM` when a time component is present; `YYYY-MM-DD` when not.

Backwards-compat read: existing CSV data in old `"Month DD, YYYY HH:MM AM/PM"` format must continue to parse. The reader normalises on load; the writer always emits the new format.

## Goals / Non-Goals

**Goals:**
- `now_str()` emits `YYYY-MM-DD HH:MM`.
- A `parse_datetime(s)` function recognises both old and new formats and returns a `datetime | None`.
- A `display_date(s)` function returns `YYYY-MM-DD HH:MM` for datetimes or `YYYY-MM-DD` for date-only values (and handles old format input via `parse_datetime`).
- `_columns.py` uses `display_date()` instead of `_date_only()`.
- `done_week.py`'s `_parse_modified()` delegates to `parse_datetime()` so both formats are grouped correctly.
- The form Due label says `YYYY-MM-DD (optional)` and on save rejects any non-empty value not matching `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`, showing an inline error `Static`.
- `tests/fixtures/tasks.csv` is migrated: `Date Created` and `Last edited time` use `YYYY-MM-DD HH:MM`; `Due` values use `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`.
- Live user data (`~/.knbn/tasks.csv`) is NOT auto-migrated; old format is accepted on read forever.

**Non-Goals:**
- A timezone-aware date type — all times remain naive local time.
- A graphical date-picker widget — plain text input with validation is sufficient given the simple terminal context.
- Migrating the `Key Resource` or other non-date fields.
- Changing the CSV column names or column order.

## Decisions

### Single `parse_datetime` in `task.py` replacing two ad-hoc parsers

`done_week.py` has its own `_parse_modified()` with a hardcoded format list. `_columns.py` has `_date_only()` doing string splitting. Both should delegate to a single `parse_datetime(s: str) -> datetime | None` in `task.py` that tries formats in order:
1. `%Y-%m-%d %H:%M` (new datetime)
2. `%Y-%m-%d` (new date-only)
3. `%B %d, %Y %I:%M %p` (old verbose datetime)
4. `%B  %d, %Y %I:%M %p` (old verbose datetime, double-space variant)

`display_date(s: str) -> str` uses `parse_datetime` to normalise, then formats back as `YYYY-MM-DD HH:MM` if minutes are non-zero or the source matched a datetime pattern, else `YYYY-MM-DD`.

**Alternative considered:** Keep per-module parsers, just update their format strings. Rejected — any future format addition would need to be made in multiple places.

### Detect "time present" by checking if source string contains `HH:MM` after the date

A stored value of `2026-07-21` has no time component; `2026-07-21 15:45` does. After parsing to a `datetime`, we check whether the original string matched a datetime pattern (not just a date pattern) to decide display format. This avoids false positives from midnight (00:00) values that happen to parse as a datetime.

Concretely: `parse_datetime` returns a `(datetime, has_time: bool)` tuple.

### Form validation: inline error `Static`, no modal

The form already has an inline layout. An `id='due-error'` `Static` rendered below the Due `Input`, normally empty, is set to a red-tinted error message when the value fails the regex `^(\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?)?$`. Save is blocked until the field is valid or empty.

**Alternative considered:** Show a `ConfirmDialog`-style modal on invalid input. Rejected — disruptive for a field-level validation.

### Fixture migration: in-place CSV rewrite

`tests/fixtures/tasks.csv` is the canonical demo dataset. Migrating it ensures tests and fresh installs see the new format. The `Due` column currently holds `DD/MM/YYYY HH:MM (TZ)` values — these are converted to `YYYY-MM-DD HH:MM` (dropping timezone suffix, converting to local wall-clock time as-is since the fixture is illustrative, not real data).

## Risks / Trade-offs

- [Risk] Users with existing `~/.knbn/tasks.csv` in old format will have their timestamps displayed in normalised form after the update — this is a cosmetic improvement not a data loss, but worth noting.
- [Trade-off] `parse_datetime` returning a tuple slightly complicates callers vs returning just `datetime | None`. Acceptable — callers need the `has_time` flag for display decisions.
