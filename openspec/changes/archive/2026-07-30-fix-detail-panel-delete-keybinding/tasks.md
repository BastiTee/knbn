## 1. Update Detail Panel Widget

- [x] 1.1 In `src/knbn/widgets/detail.py`, replace the `d` delete binding with `delete,backspace` (matching Kanban board style)
- [x] 1.2 Rename the action handler if needed so it still wires to the delete confirmation flow

## 2. Update Help Overlay

- [x] 2.1 In `src/knbn/widgets/help.py`, update the detail panel key listing: replace `d` delete entry with `Del/Bksp`

## 3. Verify

- [ ] 3.1 Launch `uv run knbn board`, open a task with `Enter`, confirm `Del` triggers delete confirmation and `d` does nothing
- [ ] 3.2 Confirm `?` help overlay shows the updated keybinding for the detail panel
