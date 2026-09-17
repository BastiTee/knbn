## Context

`KanbanView._collapsed` is a `set[str]` keyed on priority name alone. `on_lane_header_toggled` iterates every column and mutates every lane that matches the toggled priority, broadcasting the state change board-wide. `LaneHeader.Toggled` carries only `priority` and `collapsed`, so there is no column identity in the message.

See `proposal.md` for the user-facing motivation.

## Goals / Non-Goals

**Goals:**
- Scope each collapse/expand toggle to the single (column × priority) cell the user acted on.
- Preserve independent state for every cell across view recompositions.

**Non-Goals:**
- Changing any other keyboard behavior or navigation logic.
- Persisting collapse state across sessions.

## Decisions

### Key per cell with `(status, priority)` tuple

Change `_collapsed: set[str]` → `_collapsed: set[tuple[str, str]]` where the tuple is `(status, priority)`.

**Considered**: derive the status from the sender's parent widget id at toggle time. Rejected — querying the DOM to reconstruct identity that was known at construction is fragile and the extra query fires on every toggle. Passing `status` directly to `LaneHeader` is cheaper and self-documenting.

**Chosen**: extend `LaneHeader.__init__` to accept a `status: str` parameter (stored as `self._status`). Extend `LaneHeader.Toggled` to carry `status` alongside `priority`. `on_lane_header_toggled` uses `message.status` to identify the exact cell and only touches that one column/lane.

### Minimal blast radius

Only `LaneHeader` and `KanbanView` in `views/kanban.py` are changed. No other module references `LaneHeader.Toggled` or `KanbanView._collapsed`.

## Risks / Trade-offs

**Existing collapse state lost on recompose** → acceptable: collapse state already resets on any `recompose()` call (task moves, deletes, etc.). This change does not make things worse.

**`LaneHeader` gains a new required positional arg** → contained; `LaneHeader` is only instantiated inside `KanbanView.compose()`, so no call-site is missed.
