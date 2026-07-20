## Context

`KnbnApp.compose()` currently yields `Header()` as the first widget. Textual's `Header` occupies one row, displays the app title, and renders a clickable circle (the app icon) that opens the command palette. The command palette is intentionally restricted to `Ctrl+P` only; the clickable icon is an unwanted second entry point. The title row wastes vertical space in a compact terminal UI.

## Goals / Non-Goals

**Goals:**
- Remove the `Header` widget entirely, freeing one row of vertical space
- Eliminate the mouse-clickable command palette trigger

**Non-Goals:**
- Replacing the header with a custom title bar
- Changing the command palette behaviour or keybinding
- Adjusting the minimum terminal size requirement

## Decisions

### Remove Header outright rather than hiding it via CSS

`Header` can be hidden with `display: none` CSS, but it still participates in layout and keeps the DOM node. Removing it from `compose()` is cleaner and leaves no dead code.

## Risks / Trade-offs

- [No visual app title] → Acceptable; the terminal window title and context make it obvious. The `TITLE = 'knbn'` constant can stay for the terminal title bar.
