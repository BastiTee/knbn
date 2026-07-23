## Why

The current `[N]` notes indicator on Kanban cards is visually noisy ASCII. Replacing it with expressive Unicode glyphs (`☰` for notes, `※` for link) makes card metadata easier to scan at a glance. Adding `o` as a shortcut to open the key resource URL directly from the board (not just from the detail panel) reduces friction for link-heavy workflows.

## What Changes

- The notes presence indicator on Kanban cards changes from `[N]` to `☰`
- When a task also has a `key_resource` URL, the character `※` is appended (space-separated) after `☰`
- When a task has a `key_resource` URL but no notes, only `※` is shown
- Pressing `o` on a focused Kanban card opens the `key_resource` URL in the default browser (no-op if no URL is set)

## Capabilities

### New Capabilities

None — all changes are modifications to existing capabilities.

### Modified Capabilities

- `task-notes`: The notes presence indicator character changes from `[N]` to `☰`; a `※` link indicator is added alongside it when `key_resource` is set
- `tui-board`: Kanban keyboard navigation gains `o` to open the key resource URL from a focused card

## Impact

- `src/knbn/widgets/card.py`: `_notes_indicator()` logic updated to return `☰`, `※`, or both
- `src/knbn/views/kanban.py`: `o` keybinding added to open `key_resource` URL
- `openspec/specs/task-notes/spec.md`: indicator character updated in requirements and scenarios
- `openspec/specs/tui-board/spec.md`: `o` keybinding added to Kanban keyboard navigation requirement
