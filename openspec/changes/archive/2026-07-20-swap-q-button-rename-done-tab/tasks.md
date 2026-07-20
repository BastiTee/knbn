## 1. Update app bindings

- [x] 1.1 In `src/knbn/app.py`, move `Binding('q', 'quit', 'Quit', show=True)` to appear before the `1`/`2`/`3` view-switching bindings
- [x] 1.2 Change the label of `Binding('3', 'show_done_week', ...)` from `'Done/Week'` to `'Done'`

## 2. Update spec

- [x] 2.1 In `openspec/specs/tui-board/spec.md`, update the "View switching" requirement to state the `q` button appears left of the view buttons and rename all references from "Done/Week" to "Done"
- [x] 2.2 In `openspec/specs/tui-board/spec.md`, rename the "Done-by-week view" requirement heading and all internal references from "Done-by-week" / "Done/Week" to "Done"
