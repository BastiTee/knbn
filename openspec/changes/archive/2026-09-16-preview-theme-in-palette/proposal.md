## Why

Opening the theme picker (`Ctrl+P` → `Theme`) lets the user browse themes, but the only way to see what a theme actually looks like is to select it — which immediately persists it to `settings.json`. Arrowing through several themes to compare them writes the last-highlighted one to disk on every keystroke, even if the user never confirms a choice or escapes without deciding. Additionally, Textual's built-in theme picker (the command palette) is a centered overlay that covers most of the window, making it hard to see the board underneath while comparing themes.

## What Changes

- The theme picker SHALL be a sidebar docked to the right edge of the window (similar in placement to the built-in keys help panel), not a centered overlay covering most of the screen.
- While the theme sidebar is open, highlighting a theme (moving the selection with arrow keys) SHALL apply it live to the running app for preview, without writing it to `settings.json`.
- Confirming a theme (pressing `Enter`/selecting it) SHALL apply it and persist it to `settings.json`, exactly as today.
- Closing the sidebar without confirming a selection (`Esc`) SHALL revert the app's theme to whatever was active before the sidebar was opened.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `app-settings`: the Theme setting requirement gains preview semantics — highlighting a theme in the theme picker applies it live without persisting, and only a confirmed selection is written to `settings.json`; an unconfirmed preview reverts on cancel. The requirement also now specifies that the picker is a sidebar docked to the right edge of the window (leaving the rest of the board visible), not a centered overlay covering most of the screen.

## Impact

- `src/knbn/app.py`: `KnbnApp.watch_theme` persists on every `self.theme` assignment by default; `_theme_preview_active` suppresses that while previewing. `action_change_theme` now pushes a custom `ThemeSidebar` screen instead of Textual's built-in command-palette theme picker. `preview_theme`/`confirm_theme` are the public entry points the sidebar drives.
- `src/knbn/widgets/theme_sidebar.py` (new): the sidebar screen itself, built on Textual's `OptionList` docked to the right edge.
- No changes to `config.py`, `settings.json` schema, or the CLI.
