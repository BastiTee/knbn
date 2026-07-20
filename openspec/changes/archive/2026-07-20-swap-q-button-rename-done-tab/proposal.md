## Why

The footer toolbar currently shows `q` as the first button, before the three view-switching buttons (`1 Kanban`, `2 Tabular`, `3 Done/Week`). Placing quit after the navigation buttons matches the natural left-to-right reading order (navigate first, quit last) and reduces accidental quit-before-navigate confusion. The "Done/Week" label is also unnecessarily verbose — the view name "Done" is sufficient since the grouping-by-week is an implementation detail.

## What Changes

- Move the `q Quit` binding so it renders to the left of the three view buttons (`1 Kanban`, `2 Tabular`, `3 Done`) in the footer toolbar.
- Rename the `3` binding label from `Done/Week` to `Done`.

## Capabilities

### New Capabilities

<!-- None — no new capabilities introduced -->

### Modified Capabilities

- `tui-board`: View-switching toolbar order changes (q moves left of view buttons) and Done/Week view is renamed to Done in the toolbar label and view-switching requirement.

## Impact

- `src/knbn/app.py`: reorder `BINDINGS` list so `q` appears before `1`/`2`/`3`; update label for binding `3` from `'Done/Week'` to `'Done'`.
- `openspec/specs/tui-board/spec.md`: update view-switching requirement and any references to "Done/Week" → "Done".
