## Why

The footer toolbar shows keybindings for the three main tabs (1 Kanban, 2 Tabular, 3 Closed) but provides no visual feedback about which tab is currently active. Users must infer their location from the board content, which is friction — especially when switching between views rapidly.

## What Changes

- The active tab binding in the footer is visually distinguished from inactive ones (e.g. bold or highlighted style)
- The highlight updates whenever the active view changes

## Capabilities

### New Capabilities

- `active-tab-indicator`: Visual highlight on the active tab key in the footer toolbar, updating reactively as the user switches views

### Modified Capabilities

- `tui-board`: The board's footer/tab display behaviour gains an active-state requirement

## Impact

- `src/knbn/app.py`: Track current view, apply reactive style to footer bindings
- No data model or storage changes
- No new dependencies
