## Why

Keyboard navigation in the TUI has a set of bugs and gaps that make the tool feel unreliable: Shift+arrow key actions documented in the help overlay don't trigger, focus isn't automatically set on the first item when switching views, and Tab misfires as a navigation key when it should do nothing.

## What Changes

- **Auto-focus first item on view load**: all three views (Kanban, Tabular, Done-by-week) must immediately focus the first interactive item when mounted, including after view-switches.
- **Remove Tab navigation entirely**: Tab/Shift+Tab must not cycle focus between cards or rows in any view; only arrow keys navigate.
- **Shift+↑/↓ skips 10 rows in Tabular and Done views**: the documented "Up×10 / Down×10" behaviour must actually fire; currently the Shift key modifier does not reach the view action due to event-handling conflicts.
- **Focus follows moved task in Kanban**: after `Shift+↑/↓` or `Shift+←/→` repositions a card, the focused item must be the moved card in its new lane/column, not an arbitrary card.
- **Fix Shift+arrow in Kanban**: `Shift+↑/↓` must fire `action_move_up` / `action_move_down` exactly once; currently a double-dispatch between `TaskCard.on_key` and the view's `priority=True` binding causes the action to either not fire or misfire.

## Capabilities

### New Capabilities
*(none)*

### Modified Capabilities
- `tui-board`: navigation requirements updated to specify auto-focus on mount, Tab suppression, Shift+arrow reliability, and focus-follows-move semantics.

## Impact

- `src/knbn/views/kanban.py` — event-handling and `_move_and_refocus` logic
- `src/knbn/views/tabular.py` — Shift+arrow event handling
- `src/knbn/views/done_week.py` — Shift+arrow event handling
- `src/knbn/widgets/card.py` — remove manual `on_key` Shift+arrow relay
- `src/knbn/views/_row.py` — remove manual `on_key` Shift+arrow relay
- `openspec/specs/tui-board/spec.md` — updated navigation requirements
