## Context

Both table views (`TabularView`, `ClosedView`) render tasks as plain fixed-width text rows with no column header row. Users cannot tell at a glance which date column is "created" vs "edited". Additionally, the two views diverge in their group/week-header background colour: Tabular uses `$primary-darken-2` (consistent with the Kanban board palette) while Closed uses `$surface-darken-1`, making the app feel visually inconsistent.

Current column layouts:
- **Tabular**: Name, Priority, Category, Due
- **Closed**: Name, Status, Category, Priority, Last edited time, Date Created

Requested new column order for both: **Name, Status, Priority, Category, Created, Edited, Due Date**.

## Goals / Non-Goals

**Goals:**
- Add a non-focusable column-header row at the top of each table view, aligned to the data column widths.
- Reorder and rename columns in both views to: Name, Status, Priority, Category, Created, Edited, Due Date.
- Unify Closed view week-header background to `$primary-darken-2` (matching Tabular group headers).

**Non-Goals:**
- Replacing the fixed-width text rendering with a proper `DataTable` widget — the current approach is simple and sufficient.
- Changing navigation, focus, or interaction behaviour in either view.
- Altering the Kanban view.

## Decisions

### Column header as a plain Static widget

Both views already render rows as `Static`-based `TaskRow` widgets with a formatted string. The header can be a plain `Static` (non-focusable) using the exact same format string as the data rows, with column names substituted. This keeps the implementation minimal and guarantees pixel-perfect alignment at all times without a separate layout pass.

**Alternative considered:** A `Horizontal` container of proportional `Static` cells per column. Rejected — proportional layout would require migrating all row rendering to containers, significantly increasing complexity for no user-visible benefit.

### Date display: date portion only

Both `date_modified` and `date_created` are stored as `"Month DD, YYYY HH:MM AM/PM"` strings (e.g. `"July 21, 2026 03:45 PM"`). Displaying the full string in a fixed-width table would consume ~22 characters per column; with two date columns that is 44+ characters leaving too little room for Name and other columns. Each date field will be truncated to its date portion (`split(' ')[0:3]` joined, or simply the first token split on `,` year part) — specifically the characters up to and including the year, e.g. `"July 21, 2026"` (≤ 16 chars), rendered in a 16-char-wide column.

**Alternative considered:** Keep full datetime in Closed view since it's the "details" view. Rejected — the user asked for readable column headers which implies readable data; the detail panel already shows full timestamps for anyone who needs them.

### Column widths (100-column terminal, 2-char side padding)

Usable width ≈ 96 chars (padding 0 1 on view, 2-char row indent). Target layout:

| Column   | Width |
|----------|-------|
| Name     | 28    |
| Status   | 11    |
| Priority | 9     |
| Category | 14    |
| Created  | 16    |
| Edited   | 16    |
| Due      | rest  |

Total fixed: 2 indent + 28 + 1 + 11 + 1 + 9 + 1 + 14 + 1 + 16 + 1 + 16 = 101 — fits in 100 columns with Due Date elided when absent.

### Closed view Status column

Tabular already groups by status so the column is somewhat redundant there — but the user explicitly requested Status as the first data column in both views, and it aids at-a-glance scanning within a group. No change to grouping logic.

### Week-header colour alignment

Change `ClosedView`'s `.week-header` background from `$surface-darken-1` to `$primary-darken-2` to match `TabularView`'s `.group-header`. This is the only CSS change needed in `done_week.py`.

## Risks / Trade-offs

- [Risk] Narrow terminals (< 100 columns) cause column misalignment. Mitigation: the app already enforces a 100-column minimum and exits if the terminal is smaller — no additional handling needed.
- [Trade-off] Fixed-width string alignment means any future font or theme change that alters character width could misalign header and rows. Acceptable for a terminal app targeting monospace fonts.
