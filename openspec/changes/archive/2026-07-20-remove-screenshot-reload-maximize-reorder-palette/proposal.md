## Why

The app exposes several Textual built-in features that are not useful for a personal Kanban tool: the `r` Reload binding clutters the footer toolbar, and the command palette surfaces Screenshot and Maximize/Minimize commands that have no practical use here. The palette command order also puts "Quit" mid-list rather than immediately after "Theme", making the palette feel unorganised.

## What Changes

- Remove `r Reload` binding and `action_reload` method from `KnbnApp`. Task data is reloaded automatically on every view switch and after every mutation, making a manual reload redundant.
- Override `get_system_commands` in `KnbnApp` to suppress "Screenshot" and "Maximize/Minimize" palette entries.
- Override `get_system_commands` to yield "Theme" then "Quit" (then "Keys"), so Quit sits directly under Theme in the palette.
- Remove the `r` entry from the help overlay text in `HelpOverlay`.

## Capabilities

### New Capabilities

<!-- None -->

### Modified Capabilities

- `tui-board`: Remove Reload keybinding; remove Screenshot and Maximize from palette; fix palette ordering so Quit follows Theme.

## Impact

- `src/knbn/app.py`: remove `Binding('r', ...)`, `action_reload`, and `_reload_tasks` usages that are only for the reload action; add `get_system_commands` override.
- `src/knbn/widgets/help.py`: remove the `r  Reload` line from the help text.
- `openspec/specs/tui-board/spec.md`: update palette and keyboard-binding requirements.
