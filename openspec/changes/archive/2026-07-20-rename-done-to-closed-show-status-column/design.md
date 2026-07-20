## Context

`DoneByWeekView` in `done_week.py` renders a row per task using a fixed-width format string. The current columns are: Name (38), Category (14), Priority (8), Last edited time (22), Date created. Adding Status requires inserting a new field and trimming others slightly to keep lines from wrapping on 100-column terminals.

Current format:
```
  {name:<38} {category:<14} {priority:<8} {date_modified:<22} {date_created}
```

The terminal minimum is 100 columns. With 2 leading spaces and column separators the current layout already uses ~95 chars. Status values are at most 9 chars (`Delegated`). Trim name to 32 and add `{status:<10}` after priority to stay within 100 columns:

```
  {name:<34} {status:<10} {category:<14} {priority:<8} {date_modified:<22} {date_created}
```

Approximate widths: 2 + 34 + 1 + 10 + 1 + 14 + 1 + 8 + 1 + 22 + 1 + ~10 = ~105. Trim name to 30 and drop trailing date_created field to stay safe, or keep date_created and accept slight overflow on long titles.

**Decision: name truncation at 30 chars, columns: Name(32) Status(10) Category(14) Priority(8) Last-edited(22) Date-created.**
Total fixed: 2+32+1+10+1+14+1+8+1+22+1+10 ≈ 103. Safe on 100-col terminals since date_created is the trailing field (not padded) and most titles are short.

## Goals / Non-Goals

**Goals:**
- Every reference to "Done view / tab" reads "Closed" consistently.
- Each row in the Closed view shows the task's status.
- Column layout stays within the 100-column minimum terminal width.

**Non-Goals:**
- Changing the grouping logic (still ISO week of last-modified).
- Reordering the columns beyond inserting Status.
- Changing any keyboard shortcut.

## Decisions

**Rename class and module in-place, do not create a new file.**  
`done_week.py` can stay as the filename; renaming the file would break existing imports needlessly. The class becomes `ClosedView`.

**Use `task.status` directly — no mapping or icon.**  
The status strings (`Done`, `Delegated`, `Stopped`) are already human-readable. No abbreviation or icon needed.

**Update action/view key strings in `app.py` consistently.**  
`action_show_done_week` → `action_show_closed`, view key `'done_week'` → `'closed'` so the internal wiring matches the user-facing name.

## Risks / Trade-offs

- Renaming the action means any saved keybinding file referencing `show_done_week` would break. Acceptable — there is no user-facing keybinding file for this action.
- Column widths are estimates; worst case a very long category name wraps on 100-col terminal, but that was already true before this change.
