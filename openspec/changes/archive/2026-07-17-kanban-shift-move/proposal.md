## Why

Moving tasks between priorities and statuses currently requires pressing `p` or `m` and selecting from a modal prompt. This is two keystrokes plus a selection — fine for precise moves, but slow for quick triage on the board. Power users iterating through a backlog want to shunt tasks around with a single gesture. `Shift+↑`/`Shift+↓`/`Shift+←`/`Shift+→` is a natural and widely recognised "move item" pattern (cf. Trello, Jira board keyboard shortcuts, VS Code list reordering).

## What Changes

- `Shift+↑` on a focused card promotes it to the next higher priority (`Low → Medium → High`). At `High`, it is a no-op.
- `Shift+↓` demotes the card to the next lower priority (`High → Medium → Low`). At `Low`, it is a no-op.
- `Shift+←` moves the card to the previous active status column (column order: `Todo → Now → Feedback`). At `Todo` (leftmost active column), it is a no-op.
- `Shift+→` moves the card to the next active status column (`Todo → Now → Feedback`). At `Feedback` (rightmost active column), it is a no-op. **`Done`, `Delegated`, and `Stopped` are never reachable via this gesture.**
- After any move the board recomposes and focus follows the moved card in its new position.

## Capabilities

### New Capabilities

*(none)*

### Modified Capabilities

- `tui-board`: The "Keyboard navigation on board" requirement gains four new Shift+arrow bindings for in-place card movement.

## Impact

- `src/knbn/views/kanban.py` — four new bindings and action methods
- `src/knbn/widgets/help.py` — Kanban section updated with Shift+arrow entries
- `openspec/specs/tui-board/spec.md` — updated Keyboard navigation requirement
