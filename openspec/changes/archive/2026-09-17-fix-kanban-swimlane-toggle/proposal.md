## Why

When the user presses Enter on a lane header in the Kanban board, the collapse/expand state is currently tracked by priority name alone (`set[str]`), so toggling one lane simultaneously collapses or expands the same-priority lane in every other column. The user expects only the specific (column × priority) cell they are focused on to change.

## What Changes

- The internal `_collapsed` state in `KanbanView` changes from `set[str]` (priority only) to `set[tuple[str, str]]` (status, priority pair), scoping each toggle to a single cell.
- `on_lane_header_toggled` is updated to resolve the originating column and only act on that lane, not broadcast to all columns.
- The `LaneHeader.Toggled` message is extended to carry the owning status so the handler can identify which cell was toggled without re-querying the widget tree.
- `compose()` checks `(status, priority)` membership instead of priority alone when deciding whether a lane renders collapsed.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities

- `tui-board`: The swim lane collapsibility requirement is tightened — toggling a lane header SHALL only affect the single (column × priority) cell it belongs to, not all lanes of the same priority.

## Impact

- `src/knbn/views/kanban.py` — all changes are self-contained here.
- `openspec/specs/tui-board/spec.md` — delta spec updates the collapsibility requirement and its scenarios.
