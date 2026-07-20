## Context

The TUI footer toolbar is rendered by Textual from the `BINDINGS` list in `KnbnApp`. The order of `Binding` entries in that list determines the left-to-right order of buttons in the footer. Currently `q Quit` is the first binding, placing it to the left of `1 Kanban`, `2 Tabular`, `3 Done/Week`. The "Done/Week" label is verbose — it exposes an implementation detail (grouping by week) that users don't need to see.

## Goals / Non-Goals

**Goals:**
- `q` appears to the left of the three view-switching buttons in the footer toolbar.
- The third view button label reads `Done` instead of `Done/Week`.
- The `tui-board` spec reflects the updated label.

**Non-Goals:**
- Changing keybindings, functionality, or any other visual element.
- Reordering anything else in the toolbar.

## Decisions

**Reorder BINDINGS by moving `q` before `1`/`2`/`3`.**  
Textual renders footer buttons left-to-right in `BINDINGS` declaration order. Moving the `Binding('q', ...)` entry to appear before the view-switching bindings is the only change needed — no CSS or layout code requires touching.

**Change label string only, not key or action.**  
`Binding('3', 'show_done_week', 'Done/Week', show=True)` → label becomes `'Done'`. The action name `show_done_week` is internal and unchanged.

## Risks / Trade-offs

- No risks. The change is purely cosmetic (label text and declaration order); behaviour, keybindings, and data are unaffected.
