## Context

See `proposal.md` for motivation. The `knbn list` command already has `--status`, `--priority`, `--category`, and `--all` filters applied in `cli.py:list_tasks`. Date parsing is handled by `parse_datetime(s) -> tuple[datetime, bool] | None` in `model/task.py`, which recognises both `YYYY-MM-DD` and `YYYY-MM-DD HH:MM`.

## Goals / Non-Goals

**Goals:**
- Add `--after DATE` flag to `knbn list` filtering on `date_modified`.
- Reuse the existing `parse_datetime` helper; no new date library.
- Invalid dates exit non-zero with a clear error (consistent with `--status` validation).

**Non-Goals:**
- `--before` or date-range filters (not requested; add later if needed).
- Filtering on `date_created` (modifying `date_modified` covers both creates and updates).

## Decisions

### Filter on `date_modified`, not `date_created`
`date_modified` is updated on every save, so `--after` surfaces all tasks with any recent activity — both newly created and recently edited. Filtering on `date_created` alone would miss tasks that were created earlier but updated recently, which is less useful for an agent catching up on activity.

### Date comparison uses `>=` (inclusive)
`--after 2026-09-01` should include tasks modified on that date, not only after it. "After" in natural language usage for date ranges is typically inclusive of the boundary date.

### Reuse `parse_datetime` for input parsing
The flag value is parsed with the existing helper. If `parse_datetime` returns `None`, the command raises `click.BadParameter`. No new dependency needed.

## Risks / Trade-offs

**Tasks with empty `date_modified`** — shouldn't occur in practice (all writes set it), but if they do `parse_datetime('')` returns `None` and the task is excluded from `--after` results. This is the correct behaviour.
