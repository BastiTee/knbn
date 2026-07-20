## Why

The Textual `Header` widget occupies a full row, displays the app title (already obvious from context), and provides a clickable circle to open the command palette — a feature intentionally restricted to `Ctrl+P` only. Removing it reclaims vertical space and eliminates the redundant palette entry point.

## What Changes

- The `Header` widget is removed from `KnbnApp.compose()`
- The command palette is still accessible via `Ctrl+P`
- One row of vertical space is freed for the board/view content

## Capabilities

### New Capabilities

*(none)*

### Modified Capabilities

- `tui-board`: The "Command palette" requirement must note that the header's mouse-clickable palette trigger is removed; `Ctrl+P` remains the sole entry point

## Impact

- `src/knbn/app.py`: Remove `yield Header()` from `compose()`, remove `Header` from imports
- No data model, storage, or CLI changes
- Minimum terminal size constraint (100×30) is unchanged
