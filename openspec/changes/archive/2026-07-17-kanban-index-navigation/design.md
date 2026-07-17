## Context

`KanbanView` tracks `_focused_col: int` (0=Now, 1=Todo, 2=Feedback) and `_focused_row: dict[int, int]` — a per-column row index. `action_focus_left`/`action_focus_right` currently change `_focused_col` and call `_focus_col_card()`, which reads `_focused_row[new_col]`. Because each column's row index is independent, the destination row is whatever was last visited in that column (defaulting to 0), ignoring the current position.

## Goals / Non-Goals

**Goals:**
- Pressing `←`/`→` carries the current row index into the target column.
- If the target column has fewer cards than the source row index, clamp to the last card.
- `↑`/`↓` within a column are unchanged.

**Non-Goals:**
- Remembering the last-visited row when returning to a column after an up/down move (the transferred index overwrites it — acceptable).
- Any visual change to the board layout.

## Decisions

**Transfer row in `action_focus_left`/`action_focus_right` before delegating to `_focus_col_card`**

The cleanest fix is two lines added to each action:

```python
def action_focus_right(self) -> None:
    current_row = self._focused_row.get(self._focused_col, 0)
    self._focused_col = min(2, self._focused_col + 1)
    self._focused_row[self._focused_col] = current_row  # transfer; _focus_col_card clamps
    self._focus_col_card()
```

`_focus_col_card` already clamps with `min(row, len(cards) - 1)` and writes the clamped value back — so no duplicate clamping logic is needed.

## Risks / Trade-offs

- No risk: the change is two-line additions to two methods, all clamping already exists downstream.
