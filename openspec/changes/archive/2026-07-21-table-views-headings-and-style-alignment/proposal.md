## Why

The Tabular and Closed table views render rows with no column headers, making it difficult to tell apart the two date fields (created vs. edited) at a glance. The Closed view also uses a noticeably different colour scheme for its group headers (`$surface-darken-1`) versus Tabular's Kanban-aligned style (`$primary-darken-2`), creating visual inconsistency across the three views.

## What Changes

- Add a sticky column-header row to both the Tabular and Closed views.
- Standardise the column order for both views: **Name → Status → Priority → Category → Created → Edited → Due Date**.
- Align the Closed view's week-header background colour to match Tabular's group-header style (`$primary-darken-2`), while keeping the Closed view's richer column set (Status, both date fields, Due Date) unchanged.

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- `tui-board`: Tabular view and Closed view requirement sections — column definitions, column order, and header-row requirement are changing.

## Impact

- `src/knbn/views/tabular.py` — add header row widget, reorder / add columns.
- `src/knbn/views/done_week.py` — add header row widget, reorder columns to match new spec, update week-header CSS to `$primary-darken-2`.
- `openspec/specs/tui-board/spec.md` — update Tabular and Closed view requirements to reflect new columns and header row.
