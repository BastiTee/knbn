## 1. Core fix

- [x] 1.1 In `action_focus_left`, capture `current_row = self._focused_row.get(self._focused_col, 0)` before changing `_focused_col`, then assign `self._focused_row[new_col] = current_row`
- [x] 1.2 Apply the same transfer in `action_focus_right`

## 2. Verify

- [x] 2.1 Run `make build` and confirm all tests pass and type-checking is clean
